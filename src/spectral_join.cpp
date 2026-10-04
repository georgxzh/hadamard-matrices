// Exact integer spectral bounds and a full-key, multiplicity-preserving join.
// Domain intentionally restricted to the validated small lengths (no p=37).
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif
using Clock=std::chrono::steady_clock;
using Bounds=std::array<std::array<int64_t,4>,21>;
struct Entry { uint64_t hash,mask; std::array<int8_t,20> key{}; uint32_t next; };
struct Stats {
    uint64_t expected=0,nodes=0,leaves=0,accepted=0,full_rejections=0,
             prefix_conflicts=0,excluded_completions=0;
    bool complete=false; double seconds=0;
};
struct Row {
    std::vector<int> compressed,active;
    std::vector<std::array<uint64_t,3>> masks;
    std::vector<std::array<Bounds,3>> contributions;
    std::vector<std::array<Bounds,3>> transitions;
    Bounds initial{};
    uint64_t fixed=0;
};
uint64_t power3(int k) { uint64_t v=1; while(k-->0) v*=3; return v; }
int paf(uint64_t mask,int s,int length) {
    uint64_t full=(uint64_t(1)<<length)-1;
    uint64_t rotated=((mask>>s)|(mask<<(length-s)))&full;
    return length-2*__builtin_popcountll(mask^rotated);
}
uint64_t peak_memory() {
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS c{}; c.cb=sizeof(c);
    if(GetProcessMemoryInfo(GetCurrentProcess(),&c,sizeof(c))) return c.PeakWorkingSetSize;
#endif
    return 0;
}
int main(int argc,char**argv) {
 try {
    if(argc!=3) throw std::runtime_error("input and output paths required");
    std::ifstream in(argv[1]); int n,frequency_count,mode,probe; int64_t scale;
    double seconds; uint64_t node_cap,stored_cap,solution_cap;
    in>>n>>scale>>frequency_count;
    if((n!=9 && n!=15 && n!=21)||scale!=1048576||frequency_count>21)
        throw std::runtime_error("unsupported domain or scale");
    int length=3*n; std::array<Row,2> rows;
    for(auto&r:rows) { r.compressed.resize(n); for(int&v:r.compressed) in>>v; }
    std::vector<std::vector<int64_t>> cosines(frequency_count,std::vector<int64_t>(length));
    auto sines=cosines;
    for(auto&f:cosines) for(auto&v:f) in>>v;
    for(auto&f:sines) for(auto&v:f) in>>v;
    in>>mode>>probe>>seconds>>node_cap>>stored_cap>>solution_cap;
    if(!in||mode<0||mode>2||seconds<=0||seconds>1500||node_cap==0||stored_cap==0||solution_cap==0)
        throw std::runtime_error("invalid bounded configuration");
    for(auto&r:rows) {
        std::vector<int> base(length);
        for(int i=0;i<n;i++) {
            int c=r.compressed[i]; if(c!=1&&c!=-1&&c!=3&&c!=-3) throw std::runtime_error("invalid row");
            int b=c>0?1:-1;
            for(int a=0;a<3;a++) {base[i+a*n]=b; if(c==-3) r.fixed|=uint64_t(1)<<(i+a*n);}
            if(std::abs(c)==1) {
                r.active.push_back(i); std::array<uint64_t,3> choices{};
                uint64_t full=0; for(int a=0;a<3;a++) full|=uint64_t(1)<<(i+a*n);
                for(int a=0;a<3;a++) choices[a]=c==1?(uint64_t(1)<<(i+a*n)):(full^(uint64_t(1)<<(i+a*n)));
                r.masks.push_back(choices); std::array<Bounds,3> contribution{};
                for(int a=0;a<3;a++) for(int f=0;f<frequency_count;f++) {
                    contribution[a][f][0]=-2*b*cosines[f][i+a*n];
                    contribution[a][f][1]=-2*b*sines[f][i+a*n];
                }
                r.contributions.push_back(contribution);
            }
        }
        if(r.active.empty()) throw std::runtime_error("active anchor required");
        for(int f=0;f<frequency_count;f++) {
            int64_t real=0,imaginary=0;
            for(int i=0;i<length;i++) {real+=base[i]*cosines[f][i]; imaginary+=base[i]*sines[f][i];}
            r.initial[f]={real,real,imaginary,imaginary};
            for(size_t v=0;v<r.active.size();v++) {
                for(int component=0;component<2;component++) {
                    auto value=[&](int a){return r.contributions[v][a][f][component];};
                    int64_t lo=v==0?value(0):std::min({value(0),value(1),value(2)});
                    int64_t hi=v==0?value(0):std::max({value(0),value(1),value(2)});
                    r.initial[f][2*component]+=lo; r.initial[f][2*component+1]+=hi;
                }
            }
        }
        r.transitions.resize(r.active.size());
        for(size_t v=0;v<r.active.size();v++) for(int a=0;a<3;a++)
            for(int f=0;f<frequency_count;f++) for(int component=0;component<2;component++) {
                auto value=[&](int h){return r.contributions[v][h][f][component];};
                int64_t lo=std::min({value(0),value(1),value(2)}),hi=std::max({value(0),value(1),value(2)});
                r.transitions[v][a][f][2*component]=value(a)-lo;
                r.transitions[v][a][f][2*component+1]=value(a)-hi;
            }
    }
    auto start=Clock::now(); auto elapsed=[&](){return std::chrono::duration<double>(Clock::now()-start).count();};
    std::string stop="exhausted";
    int stored=rows[0].active.size()<=rows[1].active.size()?0:1;
    std::array<Stats,2> stats;
    std::vector<Entry> entries; std::vector<uint32_t> heads(1024,UINT32_MAX);
    std::vector<std::array<uint64_t,2>> solutions;
    auto spectral_conflict=[&](const Bounds&bounds) {
        int64_t threshold=scale*scale*(2*length+2);
        for(int f=0;f<frequency_count;f++) {
            auto distance=[&](int j) {
                int64_t lo=bounds[f][j]-length,hi=bounds[f][j+1]+length;
                return lo>0?lo:(hi<0?-hi:0);
            };
            int64_t a=distance(0),b=distance(2);
            if(a*a+b*b>threshold) return true;
        }
        return false;
    };
    auto key_of=[&](uint64_t mask,bool partner) {
        std::array<int8_t,20> key{};
        for(int s=1;s<n;s++) {int v=paf(mask,s,length); key[s-1]=int8_t(partner?-2-v:v);}
        return key;
    };
    auto hash_key=[&](const std::array<int8_t,20>&key) {
        uint64_t hash=14695981039346656037ULL;
        for(int j=0;j<n-1;j++) {hash^=uint8_t(key[j]); hash*=1099511628211ULL;}
        return hash;
    };
    auto rehash=[&]() {
        heads.assign(heads.size()*2,UINT32_MAX);
        for(uint32_t i=0;i<entries.size();i++) {
            size_t b=entries[i].hash&(heads.size()-1); entries[i].next=heads[b]; heads[b]=i;
        }
    };
    auto accept=[&](int side,uint64_t mask) {
        if(probe) return;
        auto key=key_of(mask,side!=stored); uint64_t hash=hash_key(key);
        size_t bucket=hash&(heads.size()-1);
        if(side==stored) {
            if(entries.size()>=stored_cap) {stop="stored_candidate_limit"; throw 1;}
            if(entries.size()>=heads.size()) {rehash(); bucket=hash&(heads.size()-1);}
            entries.push_back({hash,mask,key,heads[bucket]}); heads[bucket]=uint32_t(entries.size()-1);
        } else {
            for(uint32_t i=heads[bucket];i!=UINT32_MAX;i=entries[i].next) {
                const auto&e=entries[i]; if(e.hash!=hash||e.key!=key) continue;
                std::array<uint64_t,2> pair; pair[stored]=e.mask; pair[1-stored]=mask;
                for(int s=1;s<=length/2;s++) if(paf(pair[0],s,length)+paf(pair[1],s,length)!=-2)
                    throw std::runtime_error("projected match failed full PAF");
                if(solutions.size()>=solution_cap) {stop="solution_limit"; throw 1;}
                solutions.push_back(pair);
            }
        }
    };
    for(int side:{stored,1-stored}) {
        Row&r=rows[side]; Stats&t=stats[side]; t.expected=power3(int(r.active.size())-1);
        double row_start=elapsed();
        std::function<void(int,uint64_t,const Bounds&)> visit;
        visit=[&](int depth,uint64_t mask,const Bounds&bounds) {
            if(t.nodes>=node_cap) {stop="node_limit"; throw 1;}
            if((t.nodes&1023)==0 && elapsed()>=seconds) {stop="time_limit"; throw 1;}
            t.nodes++;
            bool leaf=depth==int(r.active.size());
            if((mode==2||mode==1&&leaf)&&spectral_conflict(bounds)) {
                if(leaf) {t.leaves++; t.full_rejections++;}
                else {t.prefix_conflicts++; t.excluded_completions+=power3(int(r.active.size())-depth);}
                return;
            }
            if(leaf) {t.leaves++; accept(side,mask); t.accepted++; return;}
            for(int a=0;a<3;a++) {
                if(mode==0) {visit(depth+1,mask|r.masks[depth][a],bounds); continue;}
                Bounds child=bounds;
                for(int f=0;f<frequency_count;f++) for(int j=0;j<4;j++)
                    child[f][j]+=r.transitions[depth][a][f][j];
                visit(depth+1,mask|r.masks[depth][a],child);
            }
        };
        try {
            visit(1,r.fixed|r.masks[0][0],r.initial); t.complete=true;
            if(t.leaves+t.excluded_completions!=t.expected) throw std::runtime_error("coverage mass mismatch");
        } catch(int) {}
        t.seconds=elapsed()-row_start;
        if(!t.complete&&!probe) break;
    }
    bool complete=stats[0].complete&&stats[1].complete&&!probe;
    std::sort(solutions.begin(),solutions.end());
    if(std::adjacent_find(solutions.begin(),solutions.end())!=solutions.end()) throw std::runtime_error("duplicate lift");
    std::ofstream out(argv[2]); out.precision(12);
    out<<"{\"complete\":"<<(complete?"true":"false")<<",\"stop_reason\":\""<<(probe?"probe":stop)
       <<"\",\"mode\":"<<mode<<",\"probe\":"<<(probe?"true":"false")<<",\"seconds_limit\":"<<seconds
       <<",\"node_limit\":"<<node_cap<<",\"stored_candidate_limit\":"<<stored_cap
       <<",\"solution_limit\":"<<solution_cap<<",\"elapsed_seconds\":"<<elapsed()
       <<",\"stored_side\":"<<stored<<",\"canonical_lower_bound\":"<<solutions.size()
       <<",\"canonical_pairs\":"<<(complete?std::to_string(solutions.size()):"null")
       <<",\"ordered_pairs\":"<<(complete?std::to_string(9*solutions.size()):"null")
       <<",\"table_entries\":"<<entries.size()<<",\"table_capacity_bytes\":"<<(entries.capacity()*sizeof(Entry)+heads.size()*sizeof(uint32_t))
       <<",\"peak_working_set_bytes\":"<<peak_memory()<<",\"rows\":[";
    for(int s=0;s<2;s++) {
        auto&t=stats[s]; if(s) out<<",";
        out<<"{\"complete\":"<<(t.complete?"true":"false")<<",\"expected\":"<<t.expected<<",\"nodes\":"<<t.nodes
           <<",\"leaves\":"<<t.leaves<<",\"accepted\":"<<t.accepted<<",\"full_rejections\":"<<t.full_rejections
           <<",\"prefix_conflicts\":"<<t.prefix_conflicts<<",\"excluded_completions\":"<<t.excluded_completions
           <<",\"elapsed_seconds\":"<<t.seconds<<"}";
    }
    out<<"],\"solutions\":[";
    for(size_t i=0;i<solutions.size();i++) {if(i)out<<","; out<<"["<<solutions[i][0]<<","<<solutions[i][1]<<"]";}
    out<<"]}\n"; if(!out) throw std::runtime_error("result write failed");
 } catch(const std::exception&e) {std::cerr<<e.what()<<"\n"; return 1;}
}

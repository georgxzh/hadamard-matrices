// Independent Cartesian binary residue enumeration, full PAF keys, sorting.
// No PhaseRow, projected-shift theorem, spectral coefficients, or pruning.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <vector>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif
using Clock=std::chrono::steady_clock;
struct Item { uint64_t fingerprint,mask; bool operator<(const Item&o)const{return fingerprint<o.fingerprint;} };
int main(int argc,char**argv) {
 try {
    if(argc!=6) throw std::runtime_error("input output candidate-cap seconds full-key required");
    std::ifstream input(argv[1]); int n; input>>n;
    if(n!=9&&n!=15&&n!=21) throw std::runtime_error("unsupported small branch");
    int length=3*n; std::vector<std::vector<int>> rows(2,std::vector<int>(n));
    for(auto&r:rows)for(auto&v:r) input>>v;
    if(!input) throw std::runtime_error("invalid input");
    uint64_t cap=std::stoull(argv[3]); double seconds=std::stod(argv[4]);
    if(!cap||seconds<=0||seconds>1400||std::string(argv[5])!="full-key") throw std::runtime_error("invalid caps");
    auto start=Clock::now(); auto elapsed=[&](){return std::chrono::duration<double>(Clock::now()-start).count();};
    std::vector<std::vector<std::vector<uint64_t>>> choices(2);
    uint64_t expected[2]={1,1},count[2]={0,0}; bool complete[2]={false,false};
    for(int side=0;side<2;side++) {
        bool anchored=false;
        for(int i=0;i<n;i++) {
            int negatives=(3-rows[side][i])/2;
            if(negatives<0||negatives>3) throw std::runtime_error("invalid compression");
            std::vector<uint64_t> parts;
            for(int bits=0;bits<8;bits++) if(__builtin_popcount(unsigned(bits))==negatives) {
                // The first nonconstant residue has minority layer zero.
                if(!anchored&&(negatives==1||negatives==2) && bool(bits&1)!=(negatives==1)) continue;
                uint64_t mask=0; for(int k=0;k<3;k++)if(bits&(1<<k)) mask|=uint64_t(1)<<(i+k*n);
                parts.push_back(mask);
            }
            if(negatives==1||negatives==2) anchored=true;
            choices[side].push_back(parts); expected[side]*=parts.size();
        }
    }
    int stored=expected[0]<=expected[1]?0:1;
    uint64_t all=(uint64_t(1)<<length)-1;
    auto key=[&](uint64_t mask,bool complement) {
        std::vector<int> result;
        int weight=__builtin_popcountll(mask);
        for(int s=1;s<=length/2;s++) {
            // Negative-support intersection identity, rather than XOR PAF.
            uint64_t shifted=((mask<<s)|(mask>>(length-s)))&all;
            int value=length-4*weight+4*__builtin_popcountll(mask&shifted);
            result.push_back(complement?-2-value:value);
        }
        return result;
    };
    auto fingerprint=[](const std::vector<int>&k) {
        uint64_t h=0x9e3779b97f4a7c15ULL;
        for(int x:k) {h^=uint64_t(x+128)+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}
        return h;
    };
    std::vector<Item> table; std::vector<std::pair<uint64_t,uint64_t>> solutions;
    double row_seconds[2]={0,0}; std::string stop="exhausted";
    for(int side:{stored,1-stored}) {
        double row_start=elapsed();
        std::function<void(int,uint64_t)> enumerate;
        enumerate=[&](int index,uint64_t mask) {
            if(count[side]>=cap) {stop="candidate_limit"; throw 1;}
            if((count[side]&4095)==0 && elapsed()>seconds) {stop="time_limit"; throw 1;}
            if(index<n) {for(uint64_t part:choices[side][index]) enumerate(index+1,mask|part); return;}
            count[side]++; auto k=key(mask,side!=stored); auto hash=fingerprint(k);
            if(side==stored) table.push_back({hash,mask});
            else {
                auto first=std::lower_bound(table.begin(),table.end(),Item{hash,0});
                for(auto it=first;it!=table.end()&&it->fingerprint==hash;it++) if(key(it->mask,false)==k) {
                    auto pair=stored==0?std::make_pair(it->mask,mask):std::make_pair(mask,it->mask);
                    solutions.push_back(pair);
                }
            }
        };
        try {enumerate(0,0); complete[side]=true;}
        catch(int) {}
        row_seconds[side]=elapsed()-row_start;
        if(side==stored) std::sort(table.begin(),table.end());
        if(!complete[side]) break;
    }
    bool done=complete[0]&&complete[1]; uint64_t peak=0;
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS c{};c.cb=sizeof(c);if(GetProcessMemoryInfo(GetCurrentProcess(),&c,sizeof(c)))peak=c.PeakWorkingSetSize;
#endif
    std::sort(solutions.begin(),solutions.end());
    if(std::adjacent_find(solutions.begin(),solutions.end())!=solutions.end())throw std::runtime_error("duplicates");
    std::ofstream output(argv[2]); output.precision(12);
    output<<"{\"complete\":"<<(done?"true":"false")<<",\"stop_reason\":\""<<stop<<"\",\"elapsed_seconds\":"<<elapsed()
          <<",\"expected\":["<<expected[0]<<","<<expected[1]<<"],\"enumerated\":["<<count[0]<<","<<count[1]
          <<"],\"row_seconds\":["<<row_seconds[0]<<","<<row_seconds[1]<<"],\"peak_working_set_bytes\":"<<peak
          <<",\"canonical_pairs\":"<<(done?std::to_string(solutions.size()):"null")
          <<",\"ordered_pairs\":"<<(done?std::to_string(9*solutions.size()):"null")<<",\"solutions\":[";
    for(size_t i=0;i<solutions.size();i++){if(i)output<<",";output<<"["<<solutions[i].first<<","<<solutions[i].second<<"]";}
    output<<"]}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}
}

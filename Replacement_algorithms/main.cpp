#include <iostream>
#include <string>
#include <iomanip>
#include <vector>
#include <algorithm>
//todo how to check one function without running all the code
unsigned int fifo(int&frameN,std::vector<int>&pages);
unsigned int lru(int&frameN,std::vector<int>&pages);
unsigned int clock(int&frameN,std::vector<int>&pages);
unsigned int opt(int&frameN,std::vector<int>&pages);
//enum rep + hashit function=> encoding method string
enum rep_alg {FIFO,OPTIMAL,LRU,CLOCK,ERROR=-1};
rep_alg hashit (std::string const& method) {
    if (method == "FIFO") return FIFO;
    else if (method == "OPTIMAL") return OPTIMAL;
    else if (method == "LRU") return LRU;
    else if (method == "CLOCK") return CLOCK;
    else return ERROR;
}
//use template instead of sending 2 parameters
template <typename type>
void inline tableprint(type toPrint)
{
    if(std::is_same<type,std::string>::value) {
        std::cout << "Replacement Policy = " << toPrint << std::endl << std::setfill('-') << std::setw(35) << "\n";
        std::cout << "Page"<<std::setfill(' ') << std::setw(6) <<""<< "Content of Frames"<<std::endl;
        std::cout << "----" << std::setfill(' ')<< std::setw(6) <<""<< std::setfill('-') << std::setw(17) <<""<<std::endl;
    }
    else
    {
        std::cout <<std::setfill('-') << std::setw(35) << "\n";
        std::cout <<"Number of page faults = "<<toPrint;
    }
}
//main as parser
int main() {
    std::string method;
    int framesNum,input;
    std::vector<int> pages;
    std::cin>>framesNum>>method;
    while ((std::cin >> input) && input != -1)
        pages.push_back(input);
    switch(hashit(method))
    {
        case 0 :
            tableprint(method);
            tableprint(fifo(framesNum,pages));
            break;
        case 1 :
            tableprint(method);
            tableprint(opt(framesNum,pages));
            break;
        case 2 :
            tableprint(method);
            tableprint(lru(framesNum,pages));
            break;
        case 3 :
            tableprint(method);
            tableprint(clock(framesNum,pages));
            break;
        default:
            perror("Replacement algorithm not found");
    }
    return 0;
}
//todo: search why capacity increase with each loop iteration.
unsigned int fifo(int&frameN,std::vector<int>&pages)
{
    unsigned int faults=0,index=0;bool fault;
    std::vector<unsigned int>frames;
    frames.reserve(frameN);
    for(auto item:pages)
    {
        fault= false;
        if(!std::count(frames.begin(), frames.end(), item)) {
            if (frames.size()!=frameN) frames.push_back(item);
            else {
                fault = true;
                faults++;
                frames[index] = item;
                index = (++index) % frameN;
            }
        }
        std::cout << std::setw(2) << std::setfill('0')<<item<<std::setw(2) <<
        std::setfill(' ')<<(fault?" F":"")<<std::setfill(' ')<< std::setw(6) <<"";
        for(auto i:frames)
            std::cout<<std::setw(2) << std::setfill('0')<<i<<" ";
        std::cout<<std::endl;
    }
    return faults;
}
unsigned int clock(int&frameN,std::vector<int>&pages)
{
    unsigned int faults=0,index=0;bool fault;
    std::vector<std::pair<unsigned int,bool>>frames;
    frames.reserve(frameN);
    for(auto item:pages)
    {
        fault= false;
        if(auto it = std::find_if(frames.begin(),frames.end(),
            [&](const auto& pair) { return pair.first == item; });it!=frames.end())
            it->second=true;
        else
        {
            if (frames.size()!=frameN) frames.push_back(std::make_pair(item,true));
            else {
                fault = true;faults++;
                while (frames[index].second)
                {
                    frames[index].second=false;
                    index = (++index) % frameN;
                }
                frames[index]= std::make_pair(item,true);
                index = (++index) % frameN;
            }
        }
        std::cout << std::setw(2) << std::setfill('0')<<item<<std::setw(2) <<
        std::setfill(' ')<<(fault?" F":"")<<std::setfill(' ')<< std::setw(6) <<"";
        for(auto i:frames)
            std::cout<<std::setw(2) << std::setfill('0')<<i.first<<" ";
        std::cout<<std::endl;
    }
    return faults;
}
unsigned int lru(int&frameN,std::vector<int>&pages)
{
    unsigned int faults=0,count=0;bool fault;
    std::vector<std::pair<unsigned int,unsigned int>>frames;
    frames.reserve(frameN);
    for(auto item:pages)
    {
        fault= false;
        if(auto it = std::find_if(frames.begin(),frames.end(),
                                  [&](const auto& pair) { return pair.first == item; });it!=frames.end())
            it->second=count++;
        else
        {
            if (frames.size()!=frameN) frames.push_back(std::make_pair(item,count++));
            else {
                fault = true;faults++;
                auto it = std::min_element(frames.begin(), frames.end(), []( const auto& lhs,const  auto& rhs) {
                    return lhs.second < rhs.second;});
                *it= std::make_pair(item,count++);
            }
        }
        std::cout << std::setw(2) << std::setfill('0')<<item<<std::setw(2) <<
        std::setfill(' ')<<(fault?" F":"")<<std::setfill(' ')<< std::setw(6) <<"";
        for(auto i:frames)
            std::cout<<std::setw(2) << std::setfill('0')<<i.first<<" ";
        std::cout<<std::endl;
    }
    return faults;
}
unsigned int opt(int&frameN,std::vector<int>&pages)
{
    unsigned int faults=0;bool fault;
    std::vector<unsigned int>frames;
    frames.reserve(frameN);
    for (auto it = pages.begin(); it != pages.end(); it++) {
        fault= false;
        if(!std::count(frames.begin(), frames.end(), *it)) {
            if (frames.size()!=frameN) frames.push_back(*it);
            else {
                unsigned int minV=0,index;
                fault = true;faults++;
                for(int i=0;i<frames.size();i++)
                {
                    unsigned temp = std::find(it, pages.end(),frames[i])-pages.begin();
                    if(temp>minV){minV=temp;index=i;}
                }
                frames[index] = *it;
            }
        }
        std::cout << std::setw(2) << std::setfill('0')<<*it<<std::setw(2) <<
        std::setfill(' ')<<(fault?" F":"")<<std::setfill(' ')<< std::setw(6) <<"";
        for(auto i:frames)
            std::cout<<std::setw(2) << std::setfill('0')<<i<<" ";
        std::cout<<std::endl;
    }
    return faults;
}
int inline find_min(std::unordered_map<unsigned int, unsigned int>&freq,std::vector<unsigned int>& frames){
    int min=INT16_MAX,index;
    for(int i=0;i<frames.size();i++)
        if(freq[frames[i]]<min) {
            min = freq[frames[i]];
            index = i;
        }
    return index;
}
//testing another methodology
unsigned int lfu(int&frameN,std::vector<int>&pages)
{
    //    building the freq hashmap
    std::unordered_map<unsigned int, unsigned int>freq;
    for(auto item:pages) freq[item]++;
    unsigned int faults=0;
    std::vector<unsigned int>frames;
    frames.reserve(frameN);
    bool fault;
    for(auto item:pages)
    {
        fault= false;
        if(std::count(frames.begin(), frames.end(), item))
            freq[item]--;
        else
        {
            if (frames.size()!=frameN){ frames.push_back(item);freq[item]--;}
            else {
                fault = true;
                faults++;
                frames[find_min(freq,frames)]=item;
            }
        }
        std::cout << std::setw(2) << std::setfill('0')<<item<<std::setw(2) <<
        std::setfill(' ')<<(fault?" F":"")<<std::setfill(' ')<< std::setw(6) <<"";
        for(auto i:frames)
            std::cout<<std::setw(2) << std::setfill('0')<<i<<" ";
        std::cout<<std::endl;
    }
    return faults;
}
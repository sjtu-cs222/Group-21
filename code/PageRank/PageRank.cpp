#include <iostream>
#include<fstream>
#include <cassert>
#include <string>
#include <vector>
#include <sstream>
#include <cmath>
using namespace std;
class pagerank
{
private:
    struct node
    {
        int num;
        double gailv;
        node *next;
        node(int number,double g,node *NEXT=NULL){num=number;gailv=g;next=NEXT;}
        node(){num=0;gailv=0;next=NULL;}
    };
    node *net;
    double *r,r0;
    int n;
    void SplitString(const string& s, vector<string>& v, const string& c)
    {
        string::size_type pos1, pos2;
        pos2 = s.find(c);
        pos1 = 0;
        while(string::npos != pos2)
        {
            v.push_back(s.substr(pos1, pos2-pos1));
            pos1 = pos2 + c.size();
            pos2 = s.find(c, pos1);
        }
        if(pos1 != s.length())
            v.push_back(s.substr(pos1));
    }
public:
    pagerank()
    {
        n=0;
        r0=0;
        net=NULL;
        r=NULL;
    }
    void read(int N)
    {
        n=N;
        r0=double(1)/n;
        net=new node[n];
        r=new double[n];
        int j=0;
        while(j<n)
        {
            r[j]=double(1)/n;
            j++;
        }
        ifstream file;
        file.open("IvtLinks.txt");
        //file.open("test.txt");
        assert(file.is_open());
        int m,x;
        double y;
        string s;
        vector<string> v;
        while(getline(file,s))
        {
            //cout<<s<<endl;
            SplitString(s, v,"\t");
            //SplitString(s, v," ");
            //cout<<v.size()<<endl;
            for(vector<string>::size_type i = 0; i != v.size(); ++i)
            {
                vector<string>::size_type k=1;
                stringstream stream;
                stream<<v[i];
                stream>>m;
                //cout<<m<<endl;
                if(i<k)
                {
                    x=m;
                    net[x-1].num=m;
                }
                if(i==k)
                {
                    y=double(1)/m;
                    net[x-1].gailv=y;
                }
                if(i>k)
                {
                    net[m-1].next=new node(x,y,net[m-1].next);
                }
            }
            vector<string>().swap(v);
            //cout<<x<<endl;
            string().swap(s);
        }
        cout<<"read over"<<endl;
        file.close();
    }
    void Rank(double a,double b)
    {
        double cha,m;
        int i;
        node *p;
        while(true)
        {
            cha=0;
            i=0;
            while(i<n)
            {
                p=net[i].next;
                m=0;
                while(p)
                {
                    //cout<<i<<'\t'<<p->num<<'\t'<<p->gailv<<endl;
                    m=m+(b*p->gailv*r[p->num-1]);
                    p=p->next;
                }
                m+=(1-b)*r0;
                //cout<<m<<endl;
                cha+=fabs(m-r[i]);
                r[i]=m;
                i++;
            }
            if(cha<a)
            {
                break;
            }
        }
    }
    void show()
    {
        int i=0;
        while(i<n)
        {
            cout<<r[i]<<'\t';
            i++;
        }
        cout<<endl;
    }
    void write()
    {
        ofstream file;
        file.open("rank.txt");
        assert(file.is_open());
        int i=0;
        while(i<n)
        {
            file<<i+1<<'\t'<<r[i]<<endl;
            i++;
        }
        file.close();
    }
};
int main()
{
    pagerank pr;
    pr.read(25205178);
    pr.Rank(0.0000000001,0.85);
    //pr.show();
    pr.write();
    return 0;
}

#include <iostream>

class Test
{
    public:
        void do_some_processing()
        {
            std::cout << "Processing inside the C++ code ..." << std::endl;
        }
};

int main()
{
    Test t;
    t.do_some_processing();
    return 0;
}

extern "C" {
    Test* Test_new()
    {
        return new Test();
    }
    void Test_do_some_processing(Test* test)
    {
        test->do_some_processing();
    }
}
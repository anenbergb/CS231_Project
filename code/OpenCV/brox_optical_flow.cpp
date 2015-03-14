#include <iostream>
#include <iomanip>
#include <string>

//#include "cvconfig.h"
#include "opencv2/core/core.hpp"
#include "opencv2/core/opengl_interop.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/gpu/gpu.hpp"

using namespace std;
using namespace cv;
using namespace cv::gpu;

void getFlowField(const Mat& u, const Mat& v, Mat& flowField);

#ifdef HAVE_OPENGL

void needleMapDraw(void* userdata);

#endif

int main(int argc, const char* argv[])
{
    try
    {
        const char* keys =
           "{ h  | help      | false | print help message }"
           "{ l  | left      |       | specify left image }"
           "{ r  | right     |       | specify right image }"
           "{ s  | scale     | 0.8   | set pyramid scale factor }"
           "{ a  | alpha     | 0.197 | set alpha }"
           "{ g  | gamma     | 50.0  | set gamma }"
           "{ i  | inner     | 10    | set number of inner iterations }"
           "{ o  | outer     | 77    | set number of outer iterations }"
           "{ si | solver    | 10    | set number of basic solver iterations }"
           "{ t  | time_step | 0.1   | set frame interpolation time step }"
            "{ sa | save     |       | location to save dX and dY }"
            "{ GPU | GPU     |       | specify GPU device id}";

        CommandLineParser cmd(argc, argv, keys);

        if (cmd.get<bool>("help"))
        {
            cout << "Usage: brox_optical_flow [options]" << endl;
            cout << "Avaible options:" << endl;
            cmd.printParams();
            return 0;
        }

        string frame0Name = cmd.get<string>("left");
        string frame1Name = cmd.get<string>("right");
        float scale = cmd.get<float>("scale");
        float alpha = cmd.get<float>("alpha");
        float gamma = cmd.get<float>("gamma");
        int inner_iterations = cmd.get<int>("inner");
        int outer_iterations = cmd.get<int>("outer");
        int solver_iterations = cmd.get<int>("solver");
        float timeStep = cmd.get<float>("time_step");
        string saveLocation = cmd.get<string>("save");
        int GPU_ID = cmd.get<int>("GPU");

        if (frame0Name.empty() || frame1Name.empty())
        {
            cerr << "Missing input file names" << endl;
            return -1;
        }

        Mat frame0Color = imread(frame0Name);
        Mat frame1Color = imread(frame1Name);

        if (frame0Color.empty() || frame1Color.empty())
        {
            cout << "Can't load input images" << endl;
            return -1;
        }
        
        cv::gpu::setDevice(GPU_ID);
        //cout << "Using GPU ID " << GPU_ID << endl;
        
        frame0Color.convertTo(frame0Color, CV_32F, 1.0 / 255.0);
        frame1Color.convertTo(frame1Color, CV_32F, 1.0 / 255.0);

        Mat frame0Gray, frame1Gray;

        cvtColor(frame0Color, frame0Gray, COLOR_BGR2GRAY);
        cvtColor(frame1Color, frame1Gray, COLOR_BGR2GRAY);

        GpuMat d_frame0(frame0Gray);
        GpuMat d_frame1(frame1Gray);

        //create optical flow object.
        BroxOpticalFlow d_flow(alpha, gamma, scale, inner_iterations, outer_iterations, solver_iterations);

        GpuMat d_fu, d_fv; //prepare recieving variables.
    
        d_flow(d_frame0, d_frame1, d_fu, d_fv);
        
        //download flow from GPU
        cv::Mat FlowX;
        cv::Mat FlowY;
        d_fu.download(FlowX);
        d_fv.download(FlowY);
        
        FlowX = abs(FlowX);
        FlowY = abs(FlowY);
        
        //compute min and max of the matrix.
        double flowX_min;
        double flowX_max;
        cv::minMaxLoc(FlowX, &flowX_min, &flowX_max);
        double flowY_min;
        double flowY_max;
        cv::minMaxLoc(FlowY, &flowY_min, &flowY_max);

        //rescale the matrix to [0, 255]
        cv::Mat FlowX_255;
        cv::Mat FlowY_255;
        
        FlowX.convertTo(FlowX_255, CV_8U, 255.0/(flowX_max - flowX_min), -255.0*flowX_min/(flowX_max - flowX_min));
        FlowY.convertTo(FlowY_255, CV_8U, 255.0/(flowY_max - flowY_min), -255.0*flowY_min/(flowY_max - flowY_min));
   
        /**
        cout << "flowX (min: " << flowX_min << " , max: " << flowX_max << ")" << endl;
        cout << "flowY (min: " << flowY_min << " , max: " << flowY_max << ")" << endl;
        double X_min;
        double X_max;
        cv::minMaxLoc(FlowX_255, &X_min, &X_max);
        double Y_min;
        double Y_max;
        cv::minMaxLoc(FlowY_255, &Y_min, &Y_max);
        cout << "flowX_255 (min: " << X_min << " , max: " << X_max << ")" << endl;
        cout << "flowY_255 (min: " << Y_min << " , max: " << Y_max << ")" << endl;
        **/
        
        //Save the mats.
        string saveX = saveLocation+"dX.jpg";
        string saveY = saveLocation+"dY.jpg";
        imwrite(saveX,FlowX_255);
        imwrite(saveY,FlowY_255);

    }
    catch (const exception& ex)
    {
        cerr << ex.what() << endl;
        return -1;
    }
    catch (...)
    {
        cerr << "Unknow error" << endl;
        return -1;
    }

    return 0;
}

template <typename T> inline T clamp (T x, T a, T b)
{
    return ((x) > (a) ? ((x) < (b) ? (x) : (b)) : (a));
}

template <typename T> inline T mapValue(T x, T a, T b, T c, T d)
{
    x = clamp(x, a, b);
    return c + (d - c) * (x - a) / (b - a);
}

void getFlowField(const Mat& u, const Mat& v, Mat& flowField)
{
    float maxDisplacement = 1.0f;

    for (int i = 0; i < u.rows; ++i)
    {
        const float* ptr_u = u.ptr<float>(i);
        const float* ptr_v = v.ptr<float>(i);

        for (int j = 0; j < u.cols; ++j)
        {
            float d = max(fabsf(ptr_u[j]), fabsf(ptr_v[j]));

            if (d > maxDisplacement) 
                maxDisplacement = d;
        }
    }

    flowField.create(u.size(), CV_8UC4);

    for (int i = 0; i < flowField.rows; ++i)
    {
        const float* ptr_u = u.ptr<float>(i);
        const float* ptr_v = v.ptr<float>(i);


        Vec4b* row = flowField.ptr<Vec4b>(i);

        for (int j = 0; j < flowField.cols; ++j)
        {
            row[j][0] = 0;
            row[j][1] = static_cast<unsigned char> (mapValue (-ptr_v[j], -maxDisplacement, maxDisplacement, 0.0f, 255.0f));
            row[j][2] = static_cast<unsigned char> (mapValue ( ptr_u[j], -maxDisplacement, maxDisplacement, 0.0f, 255.0f));
            row[j][3] = 255;
        }
    }
}

#ifdef HAVE_OPENGL

void needleMapDraw(void* userdata)
{
    const GlArrays* arr = static_cast<const GlArrays*>(userdata);

    GlCamera camera;
    camera.setOrthoProjection(0.0, 1.0, 1.0, 0.0, 0.0, 1.0);
    camera.lookAt(Point3d(0.0, 0.0, 1.0), Point3d(0.0, 0.0, 0.0), Point3d(0.0, 1.0, 0.0));

    camera.setupProjectionMatrix();
    camera.setupModelViewMatrix();

    render(*arr, RenderMode::TRIANGLES);
}

#endif
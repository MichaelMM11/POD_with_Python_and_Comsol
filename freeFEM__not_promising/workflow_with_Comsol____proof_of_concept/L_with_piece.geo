// Gmsh project created on Tue Oct 31 21:31:42 2023
SetFactory("OpenCASCADE");

// used for L shape
L = 17;
H = 13;
l = 5;
h = 8;




// L shape
Point(1) = {0, 0, -0, 1.0};
Point(2) = {L, 0, -0, 1.0};
Point(3) = {L, h, 0, 1.0};
Point(4) = {L-l, h, 0, 1.0};
Point(5) = {L-l, H, -0, 1.0};
Point(6) = {0, H,-0, 1.0};

Line(21) = {1, 2};
Line(22) = {2, 3};
Line(23) = {3, 4};
Line(24) = {4, 5};
Line(25) = {5, 6};
Line(26) = {6, 1};

Curve Loop(31) = {21, 22, 23, 24, 25, 26};

Plane Surface(41) = {31};


//Physical Curve("a", 42) = {21};
//Physical Curve("b", 43) = {22};
//Physical Curve("c", 44) = {23};
//Physical Curve("d", 45) = {24};
//Physical Curve("e", 46) = {25};
//Physical Curve("f", 47) = {26};



// interior shape
// - for the minimum working example (MWE) everything beyond
//   this line can be deleted
// - this shape can be either variant A or variant B, whereas
//   variant A is straightofrward (just straight lines) and
//   variant B contains one arc

// used for interior shape (defect)

Coherence;

// variant A
x = 2.4;
y = 3.3;
//Point(7) = {x, y, -0, 1.0};
//Point(8) = {x+x, y, -0, 1.0};
//Point(9) = {x+x, 0.5*y, -0, 1.0};
//Line(101) = {7, 8};
//Line(102) = {8, 9};
//Line(103) = {9, 7};
//Curve Loop(201) = {101, 102, 103};
//Plane Surface(301) = {201};
//Coherence;
//Transfinite Curve {9, 7, 8} = 9 Using Progression 1;



// variant B
a = 4.4;
b = 8.3;
Point(7) = {a, b, -0, 1.0};
Point(9) = {a+a, 0.5*b, -0, 1.0};
Point(10) = {a, 0.5*b, -0, 1.0};
Point(11) = {a+a, b, -0, 1.0};
Line(101) = {7, 10};
Line(102) = {9, 10};
Bezier(103) = {9,11,7};
Curve Loop(201) = {101, 102, -103};
Plane Surface(301) = {201};
Coherence;


Transfinite Curve {7} = 20 Using Progression 1;


// used for interior shape (defect)
//rx = 3.4;
//ry = 3.2;
//Circle(27) = {rx, ry, 0, 1.25, 0, 2*Pi};
//Curve Loop(32) = {27};
//Plane Surface(42) = {32};
Coherence;
//Transfinite Curve {7} = 18 Using Progression 1;


Mesh 2;
Coherence Mesh;



//Transfinite Curve {29} = 35 Using Beta 1;
Save "t1.msh";




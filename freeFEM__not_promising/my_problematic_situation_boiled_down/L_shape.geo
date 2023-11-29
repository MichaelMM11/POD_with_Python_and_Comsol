// Gmsh project created on Thu Oct 26 00:26:46 2023
// - this file creats the geometry in gmsh and generated mesh can then
//     be exported to .msh (file -> export -> *.msh -> Version2 ASCII)
// - this generated mesh (or any other supported file) can then be
//     imported in .edp
// - list of supported files:
//     https://doc.freefem.org/documentation/mesh-generation.html
SetFactory("OpenCASCADE");

// used for L shape
L = 10;
H = 8;
l = 3;
h = 5;

// used for interior shape (defect)
x = 2.4;
y = 3.3;


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


Physical Curve("a", 42) = {21};
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

//Point(7) = {x, y, -0, 1.0};
//Point(8) = {x+x, y, -0, 1.0};
//Point(9) = {x+x, 0.5*y, -0, 1.0};


// variant A
//Line(101) = {7, 8};
//Line(102) = {8, 9};
//Line(103) = {9, 7};
//Curve Loop(201) = {101, 102, 103};
//Plane Surface(301) = {201};


// variant B
//Point(10) = {x, 0.5*y, -0, 1.0};
//Line(101) = {7, 10};
//Line(102) = {9, 10};
//Bezier(103) = {7, 8, 9};
//Curve Loop(201) = {101, 102, -103};
//Plane Surface(301) = {201};



//Coherence;
//Mesh 2;
//Coherence Mesh;

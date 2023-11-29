// Gmsh project created on Tue Oct 31 21:31:42 2023
SetFactory("OpenCASCADE");

// - capital letters for box dimension, i.e. max length and width
// - minor letters are the dimensions of the missing piece
// - instead of setting up two rectangles and remove one rectangle
//     from the other it is much more comfortable to set the points
//     with little arithmetic (has also the advantage to generate
//     different geometry by playing with point calculation
L = 17;
H = 13;
l = 5;
h = 8;

// L shape
Point(1) = {0, 0, -0, 1.0};
Point(2) = {L, 0, -0, 1.0};
Point(3) = {L, H-h, 0, 1.0};
Point(4) = {L-l, H-h, 0, 1.0};
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

// special mesh densitiy definition
Transfinite Curve {26} = 40 Using Progression 1;
Transfinite Curve {22} = 15 Using Progression 1;

Coherence;
Mesh 2;
Coherence Mesh;

Save "L_with_nothing.msh";

//+
Transfinite Curve {26} = 2 Using Progression 1;
//+
Transfinite Curve {22, 23, 24, 25, 21, 26} = 4 Using Progression 1;
//+
Transfinite Curve {26, 24, 22} = 100 Using Progression 1;
//+
Transfinite Curve {21} = 500 Using Progression 1;
//+
Recombine Surface {41};
//+
Recombine Surface {41};
//+
Transfinite Surface {41} Alternated;
//+
Transfinite Curve {26} = 10000 Using Progression 1;
//+
Transfinite Curve {24} = 1000 Using Progression 1;
//+
Transfinite Curve {25} = 2000 Using Progression 1;
//+
Transfinite Curve {22} = 3000 Using Progression 1;
//+
Transfinite Curve {21} = 4000 Using Progression 1;
//+
Transfinite Curve {26} = 8000 Using Progression 1;

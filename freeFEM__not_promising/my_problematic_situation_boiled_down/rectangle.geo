// Gmsh project created on Tue Nov 21 00:52:35 2023
SetFactory("OpenCASCADE");
L = 10;
H = 8;
l = 3;
h = 5;

Point(1) = {0, 0, -0, 1.0};
Point(2) = {L, 0, -0, 1.0};
Point(3) = {L, h, 0, 1.0};
Point(4) = {0, h, 0, 1.0};

Line(21) = {1, 2};
Line(22) = {2, 3};
Line(23) = {3, 4};
Line(24) = {4, 1};

Curve Loop(31) = {21, 22, 23, 24};
Plane Surface(41) = {31};
Physical Curve(42) = {22};

Coherence;
Transfinite Curve {22} = 20 Using Progression 1;
Mesh 2;
Coherence Mesh;

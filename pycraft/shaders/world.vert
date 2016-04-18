varying vec3  Position;

void main()
{
    vec3 sunDirection = vec3(0.5, 0.0, 0.5);
    // transform the vertex position
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    // pass through the texture coordinate
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_FrontColor = gl_Color;
}
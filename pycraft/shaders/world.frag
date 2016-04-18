uniform sampler2D tex0;
uniform vec2 pixel;
varying float shade;
varying vec3 debug;

void main() {
    vec2 pos = gl_TexCoord[0].xy;
    vec4 color = texture2D(tex0, pos);
    color *= gl_Color;
    gl_FragColor = color;
}

#pragma GCC optimize "Ofast"
#include <bits/stdc++.h>
using namespace std;

// write html img src inline (local disk)
// tested on only one file, likely slow and buggy

const string directory = "D:\\Homework\\Media Art\\CPT\\";
const string filename = "List.html";
const string outputPath = "List1.html";


const char _64[65] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
typedef unsigned char byte;
void base64(FILE* fp, FILE* of) {
	int _c;
	byte c[3], d[4]; int u = 0;
	while ((_c = getc(fp)) != EOF) {
		c[u] = _c;
		if (++u == 3) {
			d[0] = c[0] >> 2;
			d[1] = ((c[0] & 0b11) << 4) | (c[1] >> 4);
			d[2] = ((c[1] & 0b1111) << 2) | (c[2] >> 6);
			d[3] = c[2] & 0b111111;
			for (int i = 0; i < 4; i++) fputc(_64[d[i]], of);
			c[0] = c[1] = c[2] = u = 0;
		}
	}
	d[0] = c[0] >> 2;
	d[1] = ((c[0] & 0b11) << 4) | (c[1] >> 4);
	d[2] = ((c[1] & 0b1111) << 2) | (c[2] >> 6);
	d[3] = c[2] & 0b111111;
	if (u) {
		for (int i = 0; i <= u; i++) fputc(_64[d[i]], of);
		for (int i = 3; i > u; i--) fputc('=', of);
	}
}

#define skipSpace while(s[d]<=' '){if(!s[d])return;fputc(s[d++],fp);}
#define skip(n) for(int i=0;i<n;i++)fputc(s[d++],fp);
#define ls(d) (s[d]>='A'&&s[d]<='Z'?char(s[d]+32):s[d])
void writeImgInline(FILE* fp, char *s) {
	int d = 0;
	while (s[d]) {
		while (s[d] != '<') { if (!s[d]) return; fputc(s[d++], fp); }
		skip(1); skipSpace;
		if (ls(d) == 'i' && ls(d + 1) == 'm' && ls(d + 2) == 'g') {
			skip(3);
			while (s[d] != '>') {
				if (ls(d) == 's' && ls(d + 1) == 'r' && ls(d + 2) == 'c') {
					skip(3); skipSpace;
					skip(1); skipSpace;
					if (s[d] == '\'' || s[d] == '\"') {
						int d0 = d; skip(1);
						string t0, t;
						while (s[d] != s[d0]) t0.push_back(s[d]), d++;
						t = directory + t0;
						printf("%s - ", &t[0]);
						FILE* img = fopen(&t[0], "rb");
						if (!img) {
							printf("FAIL\n");
							fprintf(fp, "%s", &t0[0]);
						}
						else {
							auto getSuffix = [](string s) ->string {
								stack<char> st;
								int d = s.size() - 1;
								while (d >= 0 && s[d] != '.') st.push(s[d--]);
								if (d < 0) return "";
								string t;
								while (!st.empty()) {
									char c = st.top(); st.pop();
									t.push_back(c >= 'A' && c <= 'Z' ? c + 32 : c);
								}
								return t;
							};
							string sf = getSuffix(t);
							if (sf == "jpg" || sf == "jpe") sf = "jpeg";
							else if (sf == "pns") sf = "png";
							else if (sf == "dib" || sf == "rle") sf = "bmp";
							else if (sf == "vda" || sf == "icb" || sf == "vst") sf = "tga";
							else if (sf == "tif") sf = "tiff";
							fprintf(fp, "data:image/%s;base64,", &sf[0]);
							base64(img, fp);
							printf("SUCCESS (%s)\n", &sf[0]);
						}
					}
					else printf("HTML Representation Error at %d\n", d);
				}
				skip(1);
			}
		}
	}
}

int main() {
	ifstream ifs(directory + filename);
	if (ifs.fail()) return 0;
	string s;
	getline(ifs, s, (char)ifs.eof());
	ifs.close();
	FILE* of = fopen(&(directory + outputPath)[0], "wb");
	if (!of) return 0;
	writeImgInline(of, &s[0]);
	fclose(of);
	return 0;
}


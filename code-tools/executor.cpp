#define _EXE_RELEASE 0
#define _WIN32_GUI 0

#if !(_EXE_RELEASE||_WIN32_GUI)
#define main __main
#endif

#pragma warning(disable: 4010)

#include "source.cpp"
//#include "source1.cpp"

#define _FREOPEN_STDIN   //freopen("", "r", stdin)
#define _FREOPEN_STDOUT  freopen("stdout.txt", "w", stdout)
#define _FREOPEN_STDERR  //freopen("", "w", stderr)

#define _EXE_ARGC 0
#define _EXE_ARGV { __FILE__, "" }



#if _EXE_RELEASE

#if _WIN32_GUI
#error _EXE_RELEASE and _WIN32_GUI cannot be both true
#endif

#else  // _EXE_RELEASE

#undef main

#ifdef _MSC_BUILD
#include <crtdbg.h>
#include <cstdlib>
#else
#define _CrtSetBreakAlloc(...) {}
#define _CrtDumpMemoryLeaks(...) {}
#endif  // _MSC_BUILD

int main() {
	_CrtSetBreakAlloc(-1);

	_FREOPEN_STDIN;
	_FREOPEN_STDOUT;
	_FREOPEN_STDERR;

	int _RETURN_VAL = -1;

#if !_WIN32_GUI

#if (_EXE_ARGC>1)
	const char* argv[] = _EXE_ARGV;
	_RETURN_VAL = __main(_EXE_ARGC, const_cast<char**>(argv));
#else
	_RETURN_VAL = __main();
#endif

#else  // _WIN32_GUI

#ifdef UNICODE
	_RETURN_VAL = wWinMain(NULL, NULL, NULL, SW_RESTORE);
#else
	_RETURN_VAL = WinMain(NULL, NULL, NULL, SW_RESTORE);
#endif  // UNICODE

#endif  // _WIN32_GUI

	_CrtDumpMemoryLeaks();
	return _RETURN_VAL;
}

#endif  // !_EXE_RELEASE


main.ll: main.cpp
	clang++ -S -emit-llvm main.cpp

b.ll: b.cpp
	clang++ -S -emit-llvm b.cpp

c.ll: c.cpp
	clang++ -S -emit-llvm c.cpp

main.ll.callgraph.dot: main.ll
	opt -analyze -std-link-opts -dot-callgraph main.ll

b.ll.callgraph.dot: b.ll
	opt -analyze -std-link-opts -dot-callgraph b.ll

c.ll.callgraph.dot: c.ll
	opt -analyze -std-link-opts -dot-callgraph c.ll

test: main.ll.callgraph.dot b.ll.callgraph.dot c.ll.callgraph.dot

callgraph.png: main.ll.callgraph.dot
	cat main.ll.callgraph.dot | c++filt -n | sed 's,>,\\>,g; s,-\\>,->,g; s,<,\\<,g' | dot -Tpng -ocallgraph.png
#cat main.ll.callgraph.dot | c++filt | sed 's,>,\\>,g; s,-\\>,->,g; s,<,\\<,g' | gawk '/external node/{id=$1} $1 != id' | dot -Tpng -ocallgraph.png

all: callgraph.png

clean:
	rm *.ll
	rm *.dot
	rm *.png
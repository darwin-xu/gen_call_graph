main.ll: main.cpp
	clang++ -S -emit-llvm main.cpp

b.ll: b.cpp
	clang++ -S -emit-llvm b.cpp

c.ll: c.cpp
	clang++ -S -emit-llvm c.cpp

main.ll.callgraph.dot: main.ll
	opt -analyze -dot-callgraph main.ll
	mv callgraph.dot main.ll.callgraph.dot

#may need to remove -std-link-opts
b.ll.callgraph.dot: b.ll
	opt -analyze -dot-callgraph b.ll
	mv callgraph.dot b.ll.callgraph.dot

c.ll.callgraph.dot: c.ll
	opt -analyze -dot-callgraph c.ll
	mv callgraph.dot c.ll.callgraph.dot

test: main.ll.callgraph.dot b.ll.callgraph.dot c.ll.callgraph.dot

callgraph.png: main.ll.callgraph.dot
	cat main.ll.callgraph.dot | c++filt -n | sed 's,>,\\>,g; s,-\\>,->,g; s,<,\\<,g' | dot -Tpng -ocallgraph.png
#cat main.ll.callgraph.dot | c++filt | sed 's,>,\\>,g; s,-\\>,->,g; s,<,\\<,g' | gawk '/external node/{id=$1} $1 != id' | dot -Tpng -ocallgraph.png

all: callgraph.png

clean:
	rm *.ll
	rm *.dot
	rm *.png

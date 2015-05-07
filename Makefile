all:
	gcc -g -o main main.c 
	objcopy --only-keep-debug main main.debug 
	strip main 

clean: 
	rm main rm main.debug

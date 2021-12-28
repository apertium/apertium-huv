all:
	echo "@0@:r@0@:a" | hfst-strings2fst -p -o ra.hfst
	hfst-lexc --Werror apertium-huv.huv.lexc -o huv.lexc.hfst
	hfst-twolc apertium-huv.huv.twol -o huv.twol.hfst
	hfst-twolc apertium-huv.huv.mor.twol -o huv.mor.twol.hfst
	hfst-compose-intersect -1 huv.lexc.hfst -2 huv.twol.hfst | hfst-compose-intersect -1 - -2 huv.mor.twol.hfst | hfst-substitute -f '0:⎈' -T ra.hfst -i - -o huv.gen.hfst
	hfst-invert huv.gen.hfst | hfst-fst2fst -w -o huv.automorf.hfst 
	hfst-fst2fst -w -i huv.gen.hfst -o huv.autogen.hfst 

clean:
	rm *.hfst

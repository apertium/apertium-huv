###############################################################################
## Makefile for apertium-huv
###############################################################################

LANG1=huv
BASENAME=apertium-$(LANG1)

TARGETS_COMMON =			\
	$(LANG1).automorf.hfst		\
	$(LANG1).automorf.bin		\
	$(LANG1).automorf.att.gz	\
	$(LANG1).autogen.hfst		\
	$(LANG1).autogen.bin		\
	$(LANG1).autogen.att.gz		\
	$(LANG1).autoseg.hfst		\
	$(LANG1).autoseg.bin		

#$(LANG1).autophon.hfst		
#$(LANG1).prob		
#$(LANG1).rlx.bin

TARGETS_INTERMEDIATE = $(LANG1).mor.hfst $(LANG1).seg.hfst $(LANG1).gen.hfst

# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@

###############################################################################

#hfst-invert $< |  hfst-compose -F -1 - -2 huv.spellrelax.hfst  | hfst-invert | hfst-fst2fst -w -o $@
huv.automorf.hfst: huv.mor.hfst #huv.spellrelax.hfst
	hfst-invert $< | hfst-invert | hfst-fst2fst -w -o $@

huv.autogen.hfst: huv.gen.hfst
	hfst-compose-intersect -1 $< -2 huv.mor.twol.hfst | hfst-fst2fst -w -o $@

huv.autoseg.hfst: huv.seg.hfst 
	hfst-fst2fst -w $< -o $@

huv.mor.hfst: huv.gen.hfst huv.mor.twol.hfst
	hfst-compose-intersect -1 huv.gen.hfst -2 huv.mor.twol.hfst | hfst-realign | hfst-invert -o $@

huv.gen.hfst: huv.lexc.hfst huv.twol.hfst
	hfst-compose-intersect -1 huv.lexc.hfst -2 huv.twol.hfst | hfst-realign -o $@

huv.twol.hfst: apertium-huv.huv.twol
	hfst-twolc $< -o $@

huv.lexc.hfst: apertium-huv.huv.lexc
	hfst-lexc -A --Werror $< -o $@

huv.mor.twol.hfst: apertium-huv.huv.mor.twol
	hfst-twolc apertium-huv.huv.mor.twol -o huv.mor.twol.hfst

# kojkitʼiso:k>oj>ki>tʼis>o
huv.seg.hfst: huv.mor.hfst huv.gen.hfst
	hfst-compose -F -1 huv.mor.hfst -2 huv.gen.hfst -o huv.seg.hfst 

#huv.phon.hfst: apertium-huv.huv.phon
#	hfst-regexp2fst -S apertium-huv.huv.phon | hfst-repeat -o huv.phon.hfst

#huv.autophon.hfst: huv.mor.hfst huv.phon.hfst
#	hfst-fst2fst -w huv.phon.hfst -o huv.autophon.hfst
#	hfst-project -p upper huv.mor.hfst | hfst-compose -1 - -2 huv.phon.hfst | hfst-fst2fst -w -o huv.autophon.hfst

#huv.spellrelax.hfst: apertium-huv.huv.spellrelax 
#	hfst-regexp2fst -S -o $@ < $<

huv.rlx.bin: apertium-huv.huv.rlx
	cg-comp $< $@

$(LANG1).autogen.att.gz: $(LANG1).gen.hfst
	hfst-fst2txt $< | gzip -9 -c > $@

#hfst-invert $< |  hfst-compose -F -1 - -2 huv.spellrelax.hfst  | hfst-invert | hfst-fst2txt | gzip -9 -c > $@
$(LANG1).automorf.att.gz: $(LANG1).mor.hfst #huv.spellrelax.hfst
	hfst-invert $< | hfst-invert | hfst-fst2txt | gzip -9 -c > $@

$(LANG1).autoseg.att.gz: $(LANG1).seg.hfst
	hfst-fst2txt $< | gzip -9 -c > $@

$(LANG1).autogen.bin: $(LANG1).autogen.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autogen.att
	lt-comp lr .deps/$(LANG1).autogen.att $@

$(LANG1).automorf.bin: $(LANG1).automorf.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).automorf.att
	lt-comp lr .deps/$(LANG1).automorf.att $@

$(LANG1).autoseg.bin: $(LANG1).autoseg.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autoseg.att
	lt-comp lr .deps/$(LANG1).autoseg.att $@

#$(LANG1).prob: $(BASENAME).$(LANG1).tagged
#	apertium-tagger -s 0 -u 2 $@ $<

###############################################################################
## Distribution
###############################################################################

EXTRA_DIST=$(BASENAME).$(LANG1).lexc		\
		$(BASENAME).$(LANG1).twol	\
		$(BASENAME).$(LANG1).spellrelax \
		$(BASENAME).$(LANG1).rlx	\
		modes.xml

###############################################################################
## Installation stuff
###############################################################################
#
#   apertium_huv_dir: This is where the compiled binaries go
#   apertium_huv_srcdir: This is where the source files go

apertium_huvdir=$(prefix)/share/apertium/$(BASENAME)/
apertium_huv_srcdir=$(prefix)/share/apertium/$(BASENAME)/

EXTRA_TARGETS=

if HAVE_HFSTOSPELL
EXTRA_TARGETS += $(LANG1).zhfst
endif # HAVE_HFSTOSPELL

apertium_huv_DATA=$(TARGETS_COMMON) $(EXTRA_TARGETS) 

pkgconfigdir = $(prefix)/share/pkgconfig
pkgconfig_DATA = $(BASENAME).pc

noinst_DATA=modes/$(LANG1)-morph.mode

install-data-local: install-modes
	$(INSTALL_DATA) $(BASENAME).$(LANG1).lexc $(DESTDIR)$(apertium_huv_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).twol $(DESTDIR)$(apertium_huv_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).rlx $(DESTDIR)$(apertium_huv_srcdir)


###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON) $(TARGETS_INTERMEDIATE)
clean-local:
	-rm -rf .deps modes

###############################################################################

################################################################################
# The following configures the elements to use FMUSDK2 elements

# Folder of the shared src from the FMUSDK2 submodule
FMUSDK2_PATH = ../../fmusdk2.0.3

################################################################################
# DO NOT EDIT PAST THE FOLLOWING

# FMUSDK2 configuration

FMUSDK2_DEFINE = -DFMI_COSIMULATION -DSTANDALONE_XML_PARSER	\
	-DLIBXML_STATIC

FMUSDK2_INCLUDE = -I$(FMUSDK2_PATH)/include -I$(FMUSDK2_PATH)	\
	`xml2-config --cflags`

################################################################################
# Ocarina/PolyORB-HI/C configuration

USE_CPP_LINKER = 1

USER_CFLAGS += $(FMUSDK2_DEFINE) $(FMUSDK2_INCLUDE)
USER_LDFLAGS +=  -ldl `xml2-config --libs`

USER_OBJS += $(FMUSDK2_PATH)/src/sim_support.o ../../fmu_wrapper.o	\
	$(FMUSDK2_PATH)/src/XmlElement.o				\
	$(FMUSDK2_PATH)/src/XmlParser.o					\
	$(FMUSDK2_PATH)/src/XmlParserCApi.o

all: clone ck clean

# This will generate the class, field, method and variable csv files
ck:
	if [ -f ck-0.7.1-SNAPSHOT-jar-with-dependencies ]; then echo "CK file already exists"; else cp ../CK-CodeMetrics/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar .; fi
	if [ -d src ]; then echo "Commons-Lang Repository Already Cloned"; else make clone; fi
	java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar src

# This will clone the commons-lang project
clone:
	git clone https://github.com/apache/commons-lang
	mv commons-lang/* .
	rm -rf commons-lang

# This will remove every file except the class.csv, field.csv, method.csv and variable.csv and the makefile
# And remove every folder inside it
clean:
	find . -type f ! -name '*class*.csv' ! -name '*field*.csv' ! -name '*method*.csv' ! -name '*variable*.csv' ! -name 'Makefile' -delete
	find . -type d -empty -delete
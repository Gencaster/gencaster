# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

build-graphs: export DJANGO_SETTINGS_MODULE=gencaster.settings.test
build-graphs:
	echo "Start building model graph images"
	cd ../caster-back && python manage.py graph_models --pydot -g -o ../docs/graphs/stream.png stream
	cd ../caster-back && python manage.py graph_models --pydot -g -o ../docs/graphs/stories.png stories
	cd ../caster-back && python manage.py graph_models --pydot -g -o ../docs/graphs/voice.png voice
	cd ../caster-back && python manage.py graph_models --pydot -g -o ../docs/graphs/global.png -a
	echo "Finished building model graph images"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	make build-graphs
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

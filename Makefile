
CMD_CREATE_PYENV := . venv/bin/activate.sh


start-app:
	uvicorn main:app --reload

init-env:
	@echo "**** Starting Python Environment ****"
	$(CMD_CREATE_PYENV)
USER := $(shell whoami)
SERVICE_NAME := com.$(USER).discord_hellowork
PLIST_PATH := $(HOME)/Library/LaunchAgents/$(SERVICE_NAME).plist

setup:
	python ./launchctl_create_plist.py

load:
	@[ -f $(PLIST_PATH) ] || { echo "File not found: $(PLIST_PATH)"; \
		echo "Please run 'make setup' first"; exit 1; }
	-launchctl unload $(PLIST_PATH) 2>/dev/null
	launchctl load -w $(PLIST_PATH)

unload:
	-launchctl unload $(PLIST_PATH)

start:
	launchctl start $(SERVICE_NAME)
	@$(MAKE) status

stop:
	launchctl stop $(SERVICE_NAME)
	@$(MAKE) status

restart:
	@echo "Restarting service..."
	-launchctl stop $(SERVICE_NAME)
	sleep 1
	-launchctl start $(SERVICE_NAME)
	@$(MAKE) status

status:
	@python ./launchctl_status.py status

log:
	@python ./launchctl_status.py log

FROM node:latest

ENV PATH=$PATH:/root/.opencode/bin/

WORKDIR /

# install opencode 
COPY entrypoint.sh /oc.sh
COPY models.json /root/.config/opencode/opencode.json

RUN apt update && \
    apt install -y vim curl wget unzip cron && \
	#
	curl -fsSL https://opencode.ai/v2/install | bash && \
	#
	git clone https://github.com/TheShellLand/SKILLS.git && \
	cd SKILLS && \
	git remote add ssh git@github.com:TheShellLand/SKILLS.git && \
	cd - && \
	#
	chmod +x /oc.sh


WORKDIR /root/brain/

ENTRYPOINT ["/oc.sh"]


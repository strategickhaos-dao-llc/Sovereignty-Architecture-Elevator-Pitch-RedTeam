.PHONY: init node token yubi-ca yubi-sign

CA_DIR=./state
SWARM_CA=$(CA_DIR)/swarm-ed25519.key
SWARM_PUB=$(CA_DIR)/swarm-ed25519.pub

init:
	mkdir -p $(CA_DIR)
	[ -f $(SWARM_CA) ] || age-keygen -o $(SWARM_CA)
	age-keygen -y $(SWARM_CA) > $(SWARM_PUB)
	umask 077

node:
	@test -n "$(ID)" || (echo "ID required: make node ID=command-0"; exit 1)
	mkdir -p nodes/$(ID)
	wg genkey | tee nodes/$(ID)/wg.key | wg pubkey > nodes/$(ID)/wg.pub
	age-keygen -o nodes/$(ID)/ed25519.key
	age-keygen -y nodes/$(ID)/ed25519.key > nodes/$(ID)/ed25519.pub

token:
	@test -n "$(ID)" || (echo "ID required"; exit 1)
	@test -n "$(CAP)" || (echo 'CAP required, e.g. CAP="nats.pub:telemetry.>,nats.sub:cmd.>,matrix.role:agent,router:false,net:10.44.0.0/16"'; exit 1)
	python3 scripts/mint_token.py --ca $(SWARM_CA) --node nodes/$(ID) --cap "$(CAP)" --aud wg --ttl 24h

yubi-ca:
	# Initialize YubiHSM2 slot 0x0001 with Ed25519 for CA (requires ykhsml)
	ykhsma init --label SwarmCA --algorithm ed25519 --out $(SWARM_PUB)

yubi-sign:
	@test -n "$(ID)" && @test -n "$(CAP)"
	python3 scripts/mint_token.py --yubi 1 --node nodes/$(ID) --cap "$(CAP)" --aud wg --ttl 24h

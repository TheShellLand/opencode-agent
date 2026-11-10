# V2 model generation

import os
import json
import copy


def provider_template(name, baseUrl, models, env=[]):
	models = {x[0]: copy.deepcopy(x[1]) for x in models}
	for model in models:
		models[model]['name'] = f'{name}/{model}'

	return name, dict(
		name=name,
		package='@opencode/ai/providers/openai-compatible',
		env=env,
		settings=dict(
			baseURL=baseUrl
		),
		models=models,
	)


def model_template(
	name, 
	input=['text', 'image', 'video', 'audio'], 
	output=['text'],
	reasoning=True, 
	contextWindow=20480, 
	maxTokens=16374,
	effort=["off", "minimal", "low", "medium", "high"],
	reasoningEffort='medium'
):
	return name, dict(
		name=name,
		modalities=dict(
			input=input,
			output=output
		),
		limit=dict(
			context=contextWindow,
			output=maxTokens
		),
		capabilities=dict(
			reasoning=dict(
				supported=reasoning,
				effort=effort
			)
		),
		settings=dict(
			reasoningEffort=reasoningEffort
		),
		variants=[
			dict(
				id='fast',
				settings=dict(
					reasoningEffort='low'
				)
			),
			dict(
				id='deep',
				settings=dict(
					reasoningEffort='high',
					reasoningSummary='auto'
				)
			)
		]
	)


def build_models_config(providers, default):
	models_config = dict()
	models_config['$schema'] = 'https://opencode.ai/config.json'
	models_config['model'] = default
	models_config['notifications'] = dict(
		startupTips=False,
		onboarding=False
	)
	models_config['permissions'] = [
		{
			"action": "read",
			"resource": "*",
			"effect": "allow"
		},
		{
			"action": "write",
			"resource": "*",
			"effect": "allow"
		},
		{
			"action": "tool.use",
			"resource": "*",
			"effect": "allow"
		},
		{
			"action": "integration.use",
			"resource": "mcp:internet-search",
			"effect": "allow"
		}
	]
	models_config['providers'] = {x[0]: x[1] for x in providers} 
	return models_config


def write_models_config(config):
	with open('models.json', 'w') as file:
		file.write(json.dumps(config, indent=2))
	print(os.stat('models.json'))


def main():

	models = [
		model_template(name='gemma4:12b', contextWindow=20480, maxTokens=16374)
		#model_template(name='gemma4:12b', contextWindow=20480, maxTokens=16374)
		#model_template(name='igorls/gemma-4-12B-it-heretic-GGUF', contextWindow=20480, maxTokens=16374)
	]

	providers = (
		provider_template(name='ollama_gpu_1080ti_tailscale', baseUrl='http://100.120.42.82:11434/v1', models=models),
		provider_template(name='ollama_gpu_5070fe_tailscale', baseUrl='http://100.84.90.51:11434/v1', models=models),
		provider_template(name='ollama_gpu_5070fe_local', baseUrl='http://192.168.111.175:11434/v1', models=models),
		provider_template(name='ollama_mac', baseUrl='http://host.docker.internal:11434/v1', models=models),
		provider_template(name='ollama_docker', baseUrl='http://ollama:11434/v1', models=models),
		provider_template(name='ollama_localhost', baseUrl='http://localhost:11434/v1', models=models),
	)

	default = 'ollama_gpu_1080ti_tailscale/gemma4:12b'

	models_config = build_models_config(providers, default)

	write_models_config(models_config)

	print('OK')

	return models_config


if __name__ == "__main__":
	main()


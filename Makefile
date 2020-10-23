test_models:
	@pytest orgunits/tests/models/

test_api:
	@pytest orgunits/tests/views/

test_optimization:
	@pytest orgunits/tests/optimization/

test: test_models test_api test_optimization

.PHONY: test_models test_api test_optimization test

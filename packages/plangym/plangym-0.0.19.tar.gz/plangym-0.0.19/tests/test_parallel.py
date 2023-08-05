import numpy as np
import pytest

from plangym.api_tests import batch_size, display, TestBaseEnvironment, TestGymEnvironment
from plangym.atari import AtariEnvironment
from plangym.classic_control import ClassicControl
from plangym.parallel import BatchEnv, ExternalProcess, ParallelEnvironment


def parallel_cartpole():
    return ParallelEnvironment(
        env_class=ClassicControl, name="CartPole-v0", blocking=True, n_workers=2
    )


def parallel_pacman():
    return ParallelEnvironment(env_class=AtariEnvironment, name="MsPacman-ram-v0", n_workers=2)


environments = [parallel_cartpole, parallel_pacman]


@pytest.fixture(params=environments, scope="class")
def env(request) -> ClassicControl:
    return request.param()


class TestBatchEnv:
    def test_len(self, env):
        assert len(env._batch_env) == 2

    def test_getattr(self, env):
        assert isinstance(env._batch_env, BatchEnv)
        assert env._batch_env.observation_space is not None

    def test_getitem(self, env):
        assert isinstance(env._batch_env[0], ExternalProcess)

    def test_reset(self, env):
        obs = env._batch_env.reset(return_states=False)
        assert isinstance(obs, np.ndarray)
        indices = np.arange(len(env._batch_env._envs))
        state, obs = env._batch_env.reset(return_states=True, indices=indices)
        if env.STATE_IS_ARRAY:
            assert isinstance(state, np.ndarray)


class TestExternalProcess:
    def test_reset(self, env):
        ep = env._batch_env[0]
        obs = ep.reset(return_states=False, blocking=True)
        assert isinstance(obs, np.ndarray)
        state, obs = ep.reset(return_states=True, blocking=True)
        if env.STATE_IS_ARRAY:
            assert isinstance(state, np.ndarray)

        obs = ep.reset(return_states=False, blocking=False)()
        assert isinstance(obs, np.ndarray)
        state, obs = ep.reset(return_states=True, blocking=False)()
        if env.STATE_IS_ARRAY:
            assert isinstance(state, np.ndarray)

    def test_step(self, env):
        ep = env._batch_env[0]
        state, _ = ep.reset(return_states=True, blocking=True)
        ep.set_state(state, blocking=False)()
        action = env.sample_action()
        data = ep.step(action, dt=2, blocking=True)
        assert isinstance(data, tuple)
        state, *data = ep.step(action, state, blocking=True)
        assert len(data) > 0
        if env.STATE_IS_ARRAY:
            assert isinstance(state, np.ndarray)

        state, _ = ep.reset(return_states=True, blocking=False)()
        action = env.sample_action()
        data = ep.step(action, dt=2, blocking=False)()
        assert isinstance(data, tuple)
        state, *data = ep.step(action, state, blocking=False)()
        assert len(data) > 0

    def test_attributes(self, env):
        ep = env._batch_env[0]
        ep.observation_space
        ep.action_space.sample()
        ep.__getattr__("unwrapped")
        ep.unwrapped

from datetime import datetime

from bullethell import BulletHell
from stable_baselines3 import DQN
import torch

# def main():
#     env = BulletHell()
#     done = False
#     env.reset()
#
#     for _ in range(1000):
#         while not done:
#             action = env.action_space.sample()
#             obs, reward, done, info = env.step(action)
#             print(obs)
#             env.render()
#
#         done = False
#         env.reset()
#
#     env.close()


def main():
    torch.device("cpu")
    env = BulletHell()
    done = False

    timesteps = 10000

    model = DQN.load("bullet_man-100000", env=env)
    # model = DQN("MlpPolicy",
    #             env,
    #             verbose=1,
    #             device="cpu")

    start = datetime.now()
    #model.learn(total_timesteps=timesteps)
    #model.save(f"bullet_man-{timesteps}")

    obs = env.reset()

    n_episodes = 20
    total_reward = 0

    for n in range(n_episodes):
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
            total_reward += reward

        done = False
        obs = env.reset()

    print(f'Average Reward after {timesteps} timesteps ({n_episodes} test episodes, {total_reward} cumulative reward: '
          f'{total_reward / n_episodes}')

    env.close()


if __name__ == "__main__":
    main()

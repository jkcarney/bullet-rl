import argparse
from datetime import datetime
from bullethell import BulletHell
from stable_baselines3 import DQN
import torch
import os

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


def main(timesteps, device, overwrite):
    torch.device(device)
    env = BulletHell()
    done = False

    obs = env.reset()
    path_name = f'bullet_man-{timesteps}-{str(env.observation_space.shape)}'

    if os.path.exists(f'{path_name}.zip') and not overwrite:
        model = DQN.load(path_name, env=env, device=device)
    else:
        model = DQN("MlpPolicy",
                    env,
                    verbose=1,
                    device=device)

        model.learn(total_timesteps=timesteps)
        model.save(path_name)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timesteps", default=10000, type=int)
    parser.add_argument("-r", "--overwrite", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-d", "--device", default='cpu')
    args = parser.parse_args()
    main(args.timesteps, args.device, args.overwrite)

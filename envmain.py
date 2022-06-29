
from bullethell import BulletHell
from stable_baselines3 import DQN

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
    env = BulletHell()
    done = False

    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("bullet_man")
    obs = env.reset()

    for _ in range(1000):
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()

        done = False
        obs = env.reset()

    env.close()


if __name__ == "__main__":
    main()

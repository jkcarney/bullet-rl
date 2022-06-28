
from bullethell import BulletHell


def main():
    env = BulletHell()
    done = False
    env.reset()

    while not done:
        action = env.action_space.sample()
        # apply the action
        obs, reward, done, info = env.step(action)
        env.render()

    env.close()


if __name__ == "__main__":
    main()

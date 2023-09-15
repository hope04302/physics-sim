"""
Simulator class를 통한 물리 시뮬레이션 구현!
20 * 20 * 20 방 안에서의 공의 움직임을 관찰하는 것이 목적
"""

# pip install matplotlib
# pip install tqdm

import matplotlib.pyplot as plt

from yoon_simulator import Vector, Particle, Simulator, NUM
from tqdm import tqdm


class OneParticleInRoomSimulator(Simulator):
    """
    Simulator class를 상속하여, (0, 0, 0) ~ (20, 20, 20) 안에 구속된 공의 움직임 관찰
    """

    def __init__(self,
                 particle_v: "Vector" = Vector(),
                 cor: NUM = 1.0,
                 start_time: NUM = 0.0,
                 interval: NUM = 0.01,
                 epsilon: NUM = 1e-5) -> None:
        """
        particle(Vector): 초기 공의 속도 결정
        cor(NUM): 공, 벽 사이의 반발 계수 결정
        start_time(NUM): 초기 시간 설정
        interval(NUM): 몇 초 간격으로 연산을 시행할 지 계산
        epsilon(NUM): 미분 계산 시 미소 변위 값을 설정
        """

        super().__init__(start_time, interval, epsilon)
        self.ball = Particle(vel=particle_v)
        self.cor = float(cor)

    def update(self):

        # 중력 가속도, z축이 아래
        acc = Vector(0.0, 0.0, -9.81)

        # ball 움직이기
        self.ball.update(acc, self.interval)

        #
        if self.ball.loc.x <= 0 or self.ball.loc.x >= 20:
            self.ball.vel.x = -self.ball.vel.x * self.cor
        if self.ball.loc.y <= 0 or self.ball.loc.y >= 20:
            self.ball.vel.y = -self.ball.vel.y * self.cor
        if self.ball.loc.z <= 0 or self.ball.loc.z >= 20:
            self.ball.vel.z = -self.ball.vel.z * self.cor
        self.time += self.interval
        return self.ball.loc


if __name__ == '__main__':

    simulator = OneParticleInRoomSimulator(particle_v=Vector(5.0, 7.0, 20),    # (4.0, 5.0, 20.0)
                                           cor=0.95)                            # 0.95
    progress_time = 20  # 20

    x = [0] * progress_time * 100
    y = [0] * progress_time * 100
    z = [0] * progress_time * 100

    with tqdm(total=progress_time * 100) as pbar:
        for i in range(100 * progress_time):

            x[i], y[i], z[i] = simulator.ball.loc.to_list()
            simulator.update()

            pbar.update(1)

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    ax.scatter(x[-1], y[-1], z[-1])
    plt.show()


from typing import Union, List


NUM = Union[float, int]


class Vector:
    """
    numpy, torch.Tensor와 같은 3d vector를 저장하고, 계산할 수 있게 하는 클래스
    """

    def __init__(self,
                 x: NUM = 0.0,
                 y: NUM = 0.0,
                 z: NUM = 0.0) -> None:
        """
        x(NUM): 벡터의 x 성분. float으로 입력 권장.
        y(NUM): 벡터의 y 성분.
        z(NUM): 벡터의 z 성분.
        """
        self.__x: float = float(x)
        self.__y: float = float(y)
        self.__z: float = float(z)

    # ===========================

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, r: NUM) -> None:
        if isinstance(r, float):
            self.__x = r
        elif isinstance(r, int):
            self.__x = float(r)
        else:
            raise TypeError(f"x of Vector must be float or int, not {type(r)}")

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, r: NUM) -> None:
        if isinstance(r, float):
            self.__y = r
        elif isinstance(r, int):
            self.__y = float(r)
        else:
            raise TypeError(f"y of Vector must be float or int, not {type(r)}")

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, r: NUM) -> None:
        if isinstance(r, float):
            self.__z = r
        elif isinstance(r, int):
            self.__z = float(r)
        else:
            raise TypeError(f"z of Vector must be float or int, not {type(r)}")

    # ===========================

    def to_list(self) -> List[float]:
        """
        Vector를 리스트로 변환
        """
        return [self.x, self.y, self.z]

    def __str__(self) -> str:
        return f"Vector({self.x:.5f}, {self.y:5f}, {self.x:5f})"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: NUM) -> "Vector":
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: NUM) -> "Vector":
        return self.__mul__(other)

    def __truediv__(self, other: NUM) -> "Vector":
        return Vector(self.x / other, self.y / other, self.z / other)

    def __pos__(self) -> "Vector":
        return Vector(self.x, self.y, self.z)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __abs__(self) -> float:
        """
        벡터의 크기 계산
        """
        return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5

    def dot(self, other: "Vector") -> float:
        """
        벡터의 내적(스칼라곱, dot product) 계산
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector") -> "Vector":
        return Vector(self.y * other.z - self.z - other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)


class Particle:

    """
    3차원 상에서 운동하는 입자를 표현
    """

    def __init__(self,
                 loc: "Vector" = Vector(),
                 vel: "Vector" = Vector(),
                 acc: "Vector" = Vector()) -> None:
        """
        loc(Vector): location, 현재 위치
        vel(Vector): interval, 현재 속도
        acc(Vector): accelation, 현재 가속도
        """
        if not (isinstance(loc, Vector) or isinstance(vel, Vector), isinstance(acc, Vector)):
            raise TypeError(f"Some parameter(s) in initialize func(loc, vel, acc) have wrong type")
        self.__loc: "Vector" = loc
        self.__vel: "Vector" = vel
        self.__acc: "Vector" = acc

    # ===========================

    @property
    def loc(self) -> "Vector":
        return self.__loc

    @loc.setter
    def loc(self, r: "Vector") -> None:
        if not isinstance(r, Vector):
            raise TypeError(f"Location of Particle must be Vector, not {type(r)}")
        self.__loc = r

    @property
    def vel(self) -> "Vector":
        return self.__vel

    @vel.setter
    def vel(self, r: "Vector") -> None:
        if not isinstance(r, Vector):
            raise TypeError(f"Velocity of Particle must be Vector, not {type(r)}")
        self.__vel = r

    @property
    def acc(self) -> "Vector":
        return self.__acc

    @acc.setter
    def acc(self, r: "Vector") -> None:
        if not isinstance(r, Vector):
            raise TypeError(f"Acceleration of Particle must be Vector, not {type(r)}")
        self.__acc = r

    # ===========================

    def __str__(self):
        return f"Particle(x={self.loc}, v={self.vel}, a={self.acc})"

    def __repr__(self):
        return self.__str__()

    def move(self, interval: NUM = 1.0, by_time: bool = True) -> None:
        """
        입자의 위치(self.loc)를 정수 interval만큼 이동시킴. (벡터 크기만큼 이동 -> + 연산)

        interval(NUM): 입자가 이동하는 정도. by_time에 따라 해당 정도가 달라짐
        by_time(bool): by_time=True일 때는 interval을 이동 시간으로 취급하여 interval * self.vel만큼 이동
        by_time=False일 때는 interval을 이동 거리로 취급하여 이동 거리가 interval이 되도록 self.vel 방향으로 이동
        """

        if isinstance(interval, float) or isinstance(interval, int):
            if by_time:
                self.loc += interval * self.vel
            else:
                self.loc += interval * self.vel / abs(self.vel)

        else:
            raise TypeError(f"Interval has wrong type: {type(interval)}, not float or int")

    def accelerate(self, interval: NUM = 1.0, by_time: bool = True) -> None:
        """
        입자의 속도(self.vel)를 정수 interval만큼 가속시킴. (벡터 크기만큼 가속 -> + 연산)

        interval(NUM): 입자가 가속하는 정도. by_time에 따라 해당 정도가 달라짐
        by_time(bool): by_time=True일 때는 interval을 가속하는 시간으로 취급하여 interval * self.acc만큼 가속
        by_time=False일 때는 interval을 변하는 속력으로 취급하여 변하는 속력이 interval이 되도록 self.acc의 형태대로 변화
        """

        if isinstance(interval, float) or isinstance(interval, int):
            if by_time:
                self.vel += interval * self.acc
            else:
                self.vel += interval * self.acc / abs(self.acc)

        else:
            raise TypeError(f"Interval has wrong type: {type(interval)}, not float or int")

    def update(self, acc, interval: NUM = 1.0) -> None:
        self.acc = acc
        self.accelerate(interval)
        self.move(interval)


class Simulator:
    """
    Particle을 활용해 시뮬레이션을 진행함.
    """

    def __init__(self,
                 start_time: NUM = 0.0,
                 interval: NUM = 0.01,
                 epsilon: NUM = 1e-5):
        """
        start_time(NUM): 초기 시간 설정
        interval(NUM): 몇 초 간격으로 연산을 시행할 지 계산
        epsilon(NUM): 미분 계산 시 미소 변위 값을 설정
        """

        self.time: float = float(start_time)
        self.interval: float = float(interval)
        self.epsilon: float = float(epsilon)

    def update(self) -> "Vector":
        """
        매 프레임마다 시뮬레이션 실행
        """
        pass


if __name__ == '__main__':

    v1 = Vector(3.0, 2.0, 4.0)
    v2 = Vector(5.0, 1.0, -2.0)
    print(v1,
          v1 + v2,
          v1 - v2,
          v1 * 2,
          v1.dot(v2),
          v1.cross(v2),
          v1 == v2, sep='\n')
    print()

    p = Particle(loc=v1, vel=v2)
    print(p)

    p.acc = Vector(2.0, -2.0, 0.0)
    print(p)
    p.accelerate(interval=3, by_time=False)
    print(p)
    p.move(interval=3, by_time=False)
    print(p)



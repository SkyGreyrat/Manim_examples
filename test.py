from manim import *
import numpy as np

class CirTangle(VMobject):
    # 画一个正方形减去扇形
    def __init__(self,radius:float = 2,**kwargs):
        self.radius = radius
        super().__init__(**kwargs)

    # 重写generate_points方法，Mobject被创建时会自动调用
    def generate_points(self) -> None:
        term = Arc(self.radius,num_components=36)
        point = np.array([0.5*self.radius,0.5*self.radius,0],ndmin=2)
        term.shift([-0.5*self.radius,-0.5*self.radius,0])
        points = term.get_all_points()
        points = np.concatenate((point,points,point))
        self.set_points_as_corners(points)

class MyMobject(VMobject):
    # 两个CirTangle组成的一个基本图形
    def __init__(
        self,
        radius:float = 2,
        **kwargs,
    ):
        super().__init__(**kwargs)
        term_1 = CirTangle(radius).set_stroke(width=2,color=RED)
        term_2 = CirTangle(radius).set_stroke(width=2,color=RED)
        term_2.rotate(PI)
        self.add(term_1,term_2)

        
class Test(Scene):
    def construct(self) -> None:
        # 创建一个大的Mobject对象包含所有的小基本图形
        mobjects = [MyMobject(radius=5).set_fill(color=RED,opacity=0.2) for _ in range(6)] 
        mob = Mobject()
        mob.add(*mobjects)

        # 自己写一个Animation类，会让mob的所有子对象不同地旋转与同时地放缩
        self.play(Anime(mob),run_time=15)

class Anime(Animation):
    def __init__(
        self, 
        mobject,
        theta = 0.01*PI, # 旋转因子
        delta = 0.02, #放缩因子
        **kwargs,
    ): 
        self.theta = theta
        self.delta = delta  
        self.mobject = mobject   
        super().__init__(self.mobject,**kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # 重新动画插帧函数，转动放缩每一个子对象
        i = 1
        for m in self.mobject.submobjects:
            m.rotate(self.theta*i*alpha)
            m.scale(1-0.5*self.delta*alpha)
            i = i + 0.3
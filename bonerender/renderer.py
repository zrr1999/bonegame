#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/26 22:14
# @Author : 詹荣瑞
# @File : renderer.py
# @desc : 本代码未经授权禁止商用
import numpy as np
import moderngl_window as mglw
import moderngl
from moderngl_window.scene import Camera
from moderngl_window.context.pyglet import Window


class RendererBase(Window):
    resizable = True
    samples = 4

    def __init__(self, title="RendererBase", window_size=(1280, 720), aspect_ratio=1):
        super().__init__(title=title, gl_version=(4, 1),
                         size=window_size, aspect_ratio=aspect_ratio)
        self.mouse_scroll_event_func = self.mouse_scroll_event
        self.key_event_func = self.key_event
        self.main_program = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                in vec2 in_pos;
                in float in_scale;
                in vec4 in_color;
                uniform mat4 Mvp;
    
                out vec4 v_color;

                void main() {
                    gl_Position = Mvp*vec4(in_pos + (in_vert * in_scale), 0.0, 1.0);
                    gl_Position.xy = gl_Position.xy/(gl_Position[2]+1);
                    v_color = in_color;
                }
            ''',
            fragment_shader='''
                #version 330

                in vec4 v_color;
                out vec4 f_color;

                void main() {
                    f_color = v_color;
                }
            ''',
        )
        self.camera = Camera(fov=90, near=10, far=1000)
        self.color_buffer = self.ctx.buffer(
            np.array([[0.0, 1.0, 0.0, 1.0]], dtype='f4').tobytes()
        )
        self.scale = 0.8
        self.mvp = self.main_program['Mvp']
        self.mvp.write(self.camera.matrix)

        self.index_buffer = self.ctx.buffer(np.array([
            0, 1, 2,
            1, 2, 3
        ], 'i4').tobytes())

        self.share_cache = None
        self.w = 0
        self.h = 0

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        pos_offset = self.camera.position[2] + y_offset / 10
        print(self.camera.position[2])
        if -0.8 < pos_offset < 0.7:
            self.camera.position[2] = pos_offset

    def key_event(self, key, action, modifiers):
        if key == ord('q'):
            self.camera.yaw += 1
        elif key == ord('e'):
            self.camera.yaw -= 1
        elif key == ord('w'):
            self.camera.position[1] -= 0.01
        elif key == ord('a'):
            self.camera.position[0] += 0.01
        elif key == ord('s'):
            self.camera.position[1] += 0.01
        elif key == ord('d'):
            self.camera.position[0] -= 0.01
        # print(key, ord("d"), action, modifiers)

    def polygon(self, vertex, pos_scale=None, colors=None, dim=2):
        if colors is None:
            colors_buffer = self.color_buffer
        else:
            colors_buffer = self.ctx.buffer(colors.astype('f4').tobytes())

        if pos_scale is None:
            pos_scale = np.array([0., 0, 1], 'f4').tobytes()
        else:
            pos_scale = np.array(pos_scale).astype('f4').tobytes()
        pos_scale_buffer = self.ctx.buffer(pos_scale)

        vertex = np.array(vertex, 'f4').reshape((-1, 2))
        vertex_buffer = self.ctx.buffer(vertex.tobytes())
        n = vertex.shape[0]

        index = np.arange(n)
        index = np.c_[np.zeros(n - 2, 'i4'), index[1:-1], index[2:]]
        index_buffer = self.ctx.buffer(index.tobytes())

        vao_content = [
            (vertex_buffer, f'{dim}f', 'in_vert'),
            (colors_buffer, '4f', 'in_color'),
            (pos_scale_buffer, '2f 1f/i', 'in_pos', 'in_scale'),
        ]
        self.ctx.vertex_array(self.main_program, vao_content, index_buffer).render()

    def circle(self, center, radius, colors=None, quality=10):
        theta = np.arange(-np.pi, np.pi, 7 / quality)
        x = np.cos(theta)
        y = np.sin(theta)
        arr = np.c_[x, y]
        pos_scale = [*center, radius]
        if colors is None:
            colors = np.array([[0.0, 0.0, 0.0, 1.0]]).repeat(len(theta), 0)
        else:
            colors = np.array([colors]).repeat(len(theta), 0)
        self.polygon(arr, pos_scale=pos_scale, colors=colors)

    def grid(self, m, n=None, colors=None):
        if n is None:
            n = m
        if colors is None:
            colors_buffer = self.color_buffer
        else:
            colors_buffer = self.ctx.buffer(colors.astype('f4').tobytes())

        u1 = np.repeat(np.linspace(-1, 1, m), 2)
        v1 = np.tile([-1, 1], m)
        v2 = np.repeat(np.linspace(-1, 1, n), 2)
        u2 = np.tile([-1, 1], n)
        vertices = np.concatenate([np.c_[u1, v1], np.c_[u2, v2]], 0)

        vao_content = [
            (self.ctx.buffer(vertices.astype('f4').tobytes()), '2f', 'in_vert'),
            (self.ctx.buffer(np.array([0., 0, 1], 'f4').tobytes()), '2f 1f/i', 'in_pos', 'in_scale'),
        ]
        self.ctx.vertex_array(self.main_program, vao_content,
                              self.ctx.buffer(np.arange(vertices.shape[0]).tobytes())
                              ).render(moderngl.LINES)


class Renderer(RendererBase):

    def __init__(self, title="Renderer", height=480, width=640, colors=None):
        super(Renderer, self).__init__(title, window_size=(width, height))
        self.h = height
        self.w = width

        if colors is None:
            self.colors = ((0.082, 0.396, 0.753, 1), (0.761, 0.094, 0.357, 1), (0, 0.5, 0, 1))
        else:
            self.colors = colors

    # def __call__(self, mat, win_name):
    #     self.render(mat, win_name)


if __name__ == '__main__':
    r = Renderer()
    a = np.zeros((7, 7), np.uint8)
    a[:, :2] = 1
    a[:, 2:3] = 2
    while True:
        m, n = a.shape
        r.ctx.clear(1.0, 1.0, 1.0)
        r.mvp.write(r.camera.matrix)
        r.grid(m, n)
        for i in range(m):
            y = m - 2 * i - 1
            for j in range(n):
                x = - n + 2 * j + 1
                if a[i, j]:
                    color = r.colors[a[i, j] - 1]
                    r.circle((x / (n - 1), y / (m - 1),), 0.05, color, 12)
        r.swap_buffers()

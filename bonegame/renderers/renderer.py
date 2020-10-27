#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/10 15:55
# @Author : 詹荣瑞
# @File : renderer.py
# @desc : 本代码未经授权禁止商用
import cv2
import numpy as np
import moderngl_window as mglw
import moderngl
import os
import threading


class RendererBase(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "RendererBase"
    window_size = (1280, 720)
    aspect_ratio = 9 / 9
    resizable = True
    samples = 4

    def __init__(self):
        window_cls = mglw.get_window_cls('moderngl_window.context.pyglet.Window')
        window = window_cls(title="GoBang", gl_version=(4, 1), size=(800, 600), )
        mglw.activate_context(ctx=window.ctx)
        super().__init__(ctx=window.ctx, wnd=window)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                in vec2 in_pos;
                in float in_scale;
                in vec4 in_color;

                out vec4 v_color;

                void main() {
                    gl_Position = vec4(in_pos + (in_vert * in_scale), 0.0, 1.0);
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
        self.scale = 0.8
        color = np.array([[0.0, 1.0, 0.0, 1.0]], dtype='f4')
        self.color_buffer = self.ctx.buffer(color.tobytes())
        # self.mvp = self.prog['Mvp']
        # self.mvp.write((np.array([[self.scale, 0, 0, 0], [0, self.scale, 0, 0],
        #                           [0, 0, self.scale, 0], [0, 0, 0, 1]], dtype='f4')).tobytes())
        self.index_buffer = self.ctx.buffer(np.array([
            0, 1, 2,
            1, 2, 3
        ], 'i4').tobytes())

        self.share_cache = None
        self.w = 0
        self.h = 0

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.scale *= 1 + y_offset / 10

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
        self.ctx.vertex_array(self.prog, vao_content, index_buffer).render()

    def circle(self, center, radius, colors=None, quality=10):
        theta = np.arange(-np.pi, np.pi, 1 / quality)
        x = np.cos(theta)
        y = np.sin(theta)
        arr = np.c_[x, y]
        pos_scale = [*center, radius]
        if colors is None:
            colors = np.array([[0.0, 0.0, 0.0, 1.0]]).repeat(len(theta), 0)
        else:
            colors = np.array(colors).repeat(len(theta))
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
        return self.ctx.vertex_array(self.prog, vao_content,
                                     self.ctx.buffer(np.arange(vertices.shape[0]).tobytes())
                                     )

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.grid(7, 7).render(moderngl.LINES)
        # mat = self.share_cache
        # m, n = mat.shape
        # km, kn = self.h // m // 2, self.w // n // 2
        # out = np.zeros((self.h, self.w))
        # for i in range(m):
        #     y = 2 * i + 1
        #     for j in range(n):
        #         x = 2 * j + 1
        #         if mat[i, j]:
        #             color = 255/mat[i, j]
        #             cv2.circle(out, (x * kn, y * km, ), 20, color, -1)
        # for i in range(10):
        #     for j in range(10):
        #         self.circle(((i - 3) / 3, (j - 3) / 3), 0.05)


class Renderer(object):

    def __init__(self, height=480, width=640, colors=((0, 0, 0), (255, 0, 0), (0, 255, 0))):
        self.core = RendererBase()
        self.core.title = "GoBang"
        self.core.window_size = (width, height)
        self.core.h = height
        self.core.w = width
        # threading.Thread(target=self.core.run).start()

        self.h = height
        self.w = width
        self.colors = colors

    def __call__(self, mat, win_name):
        self.render(mat, win_name)

    def render(self, mat, win_name=None):
        self.core.render(1, 1)
        m, n = mat.shape
        # km, kn = self.h // m // 2, self.w // n // 2
        for i in range(m):
            y = 2 * i - m + 1
            for j in range(n):
                x = 2 * j - n + 1
                if mat[i, j]:
                    color = [0.0, mat[i, j] / 255, 0.0, mat[i, j] / 255]
                    self.core.circle((x / (n - 1), y / (m - 1),), 0.05, color)
        self.core.wnd.swap_buffers()
        # m, n = mat.shape
        # km, kn = self.h // m // 2, self.w // n // 2
        # out = np.zeros((self.h, self.w))
        # for i in range(m):
        #     y = 2 * i + 1
        #     for j in range(n):
        #         x = 2 * j + 1
        #         if mat[i, j]:
        #             color = 255/mat[i, j]
        #             cv2.circle(out, (x * kn, y * km, ), 20, color, -1)
        # for i in range(m):
        #     i = 2 * i + 1
        #     out = cv2.line(out, (i * km, 0), (i * km, 2 * n * kn), 255)
        # for i in range(n):
        #     i = 2 * i + 1
        #     out = cv2.line(out, (0, i * km), (2 * m * km, i * kn), 255)
        # cv2.imshow(win_name, out.astype(np.uint8))


if __name__ == '__main__':
    r = Renderer()
    a = np.zeros((7, 7), np.uint8)
    a[:, :2] = 255
    a[:, 2:3] = 155
    while True:
        r.render(a)

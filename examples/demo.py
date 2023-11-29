# ruff: noqa: T201, ERA001
import moderngl as mgl
import pygame as pg


def main():
    pg.init()
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

    pg.display.set_mode((1600, 900), flags=pg.OPENGL | pg.DOUBLEBUF)
    ctx = mgl.create_context()
    clock = pg.time.Clock()

    # pg.event.set_blocked(None)
    # pg.event.set_allowed([pg.QUIT, pg.KEYDOWN])

    print(pg.display.get_current_refresh_rate())
    running = True
    # print("Entering")
    while running:
        # print("Start:", clock.get_time())
        for ev in pg.event.get():
            # print(pg.event.event_name(ev.type))
            if ev.type == pg.QUIT or (ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE):
                running = False

        ctx.clear(0.08, 0.16, 0.18)
        pg.display.flip()
        clock.tick(60)
        # print("End:", dt, clock.get_time())

    ctx.release()
    pg.quit()


if __name__ == "__main__":
    main()

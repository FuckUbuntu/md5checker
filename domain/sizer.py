def autosize(vol):
    un = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = 1024.0
    for i in range(len(un)):
        if (vol / size) < 1:
            return "%.1f%s" % (vol, un[i])
        vol = vol / size
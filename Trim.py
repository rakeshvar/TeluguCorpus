def trim_low_counts(uni, bi, tri, to_be_removed):
    rem = {s for s, v in uni.items() if to_be_removed(s, v)}
    print("Removing: ", list((s, uni[s]) for s in rem))

    # Remove from unigrams
    for s in rem:
        uni.pop(s, None)

    # Remove from bigrams
    for s in list(bi.keys()):  # Use list to avoid modification during iteration
        if s in rem:
            bi.pop(s)
        else:
            for t in list(bi[s].keys()):
                if t in rem:
                    bi[s].pop(t)
            if not bi[s]:
                bi.pop(s)

    # Remove from trigrams
    for s in list(tri.keys()):
        if s in rem:
            tri.pop(s)
        else:
            for t in list(tri[s].keys()):
                if t in rem:
                    tri[s].pop(t)
                else:
                    for u in list(tri[s][t].keys()):
                        if u in rem:
                            tri[s][t].pop(u)
                    # Remove empty inner dicts
                    if not tri[s][t]:
                        tri[s].pop(t)
            # Remove empty middle dicts
            if not tri[s]:
                tri.pop(s)
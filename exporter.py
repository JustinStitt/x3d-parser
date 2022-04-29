def export_to_QT(_object) -> str:
    '''
    Exports objects for use in QT (C++) Ray Tracing environment
    '''
    tris_out = ''
    for tri in _object.mesh.tris:
        tris_out = tris_out + \
        ('''
        {{%s,%s,%s},{%s,%s,%s},{%s,%s,%s}},
        ''' % (*tri[0], *tri[1], *tri[2])).strip()
    tris_out = tris_out.strip()[:-1] # remove trailing spaces and comma

    translate_out = ''
    for x in _object.transform.translation.split(' '):
        translate_out = translate_out + f'{x},'
    translate_out = translate_out[:-1]
    
    final_out =\
    '''
    mesh{{%s},{%s}},
    ''' % (tris_out, translate_out)

    return final_out

def export_line_based(_object):
    for tri in _object.mesh.tris:
        for p in tri:
            print(p.x, p.y, p.z, end = ' ')
        print()

'''
Steps:
1) Combine object meshes (rect and tris) to one massive vector
2) Format into vector
'''
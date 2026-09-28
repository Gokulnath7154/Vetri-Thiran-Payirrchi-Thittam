def build_comic_layout(image_paths, full_story, outline):
    blocks=[]; current=[]
    for line in full_story.splitlines():
        if line.strip().lower().startswith("panel ") and current:
            blocks.append("\n".join(current).strip()); current=[line]
        else:
            current.append(line)
    if current: blocks.append("\n".join(current).strip())
    layout=[]
    for i,(image,panel) in enumerate(zip(image_paths,outline),1):
        rel=image.replace("\\","/").split("static/",1)[-1]
        layout.append({"panel":i,"title":panel.get("title",f"Panel {i}"),
                       "image_path":image,"image_url":"/static/"+rel,
                       "text":blocks[i-1] if i-1<len(blocks) else panel["scene_description"],
                       "scene_description":panel.get("scene_description",""),
                       "image_prompt":panel.get("image_prompt","")})
    return layout

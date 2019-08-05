using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class background_change_toggle : MonoBehaviour
{
    bool clicked;
    public Toggle toggle;
    public Sprite on;
    public Sprite off; 
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    public void change_sprite()
    {
        clicked = !clicked; 
        if (clicked == true)
        {
            toggle.image.overrideSprite = off;
        }
        else if (clicked == false)
        {
            toggle.image.overrideSprite = on;
        }
    }
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

// Changes the backgrounds for the toggles under the Sensor panel
// Takes the toggle (game object) and the two different sprites,
// in this case the off sprite and on sprite. When toggle is clicked
// it changes between the two images

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
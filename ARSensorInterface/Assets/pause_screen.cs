using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Vuforia;

public class pause_screen : MonoBehaviour
{
    bool freezeToggle;
    public Button freeze_button;
    public Sprite pause;
    public Sprite play; 
    // Start is called before the first frame update
    void Start()
    {
        VuforiaRenderer.Instance.Pause(false);
    }

    // Update is called once per frame
    public void Freeze()
    {
        freezeToggle = !freezeToggle;
        if (freezeToggle == false)
        {
            freeze_button.image.overrideSprite = pause; 
        }
        else if (freezeToggle == true)
        {
            freeze_button.image.overrideSprite = play;
        }
        VuforiaRenderer.Instance.Pause(freezeToggle);

    }
}
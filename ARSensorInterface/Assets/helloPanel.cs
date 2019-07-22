using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class helloPanel : MonoBehaviour
{
    public GameObject thisPanel;
    bool state;

    public void showPanel()
    {
        state = !state;
        thisPanel.SetActive(state);
    }
}

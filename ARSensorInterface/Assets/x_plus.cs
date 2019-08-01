using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class x_plus : MonoBehaviour
{
    public static bool x_plus_apply;

    public void change_apply()
    {
        x_plus_apply = !x_plus_apply;
    }
    public static void apply_equals_false()
    {
        x_plus_apply = false;
    }

}
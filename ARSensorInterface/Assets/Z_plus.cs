using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Z_plus : MonoBehaviour
{
    public static bool z_plus_apply;

    public void change_apply()
    {
        z_plus_apply = !z_plus_apply;
    }
    public static void apply_equals_false()
    {
        z_plus_apply = false;
    }

}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Z_minus : MonoBehaviour
{
    public static bool z_minus_apply;

    public void change_apply()
    {
        z_minus_apply = !z_minus_apply;
    }
    public static void apply_equals_false()
    {
        z_minus_apply = false;
    }

}

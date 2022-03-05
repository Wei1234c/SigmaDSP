/*
 * File:           C:\Users\Wei\Dropbox\Coding\notebooks\專案\待處理\SigmaDSP\bitbucket\github\SigmaStudio projects\projects\test\Design 1_IC_2_PARAM.h
 *
 * Created:        Saturday, March 5, 2022 3:59:36 PM
 * Description:    :IC 2 parameter RAM definitions.
 *
 * This software is distributed in the hope that it will be useful,
 * but is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * This software may only be used to program products purchased from
 * Analog Devices for incorporation by you into audio products that
 * are intended for resale to audio product end users. This software
 * may not be distributed whole or in any part to third parties.
 *
 * Copyright ©2022 Analog Devices, Inc. All rights reserved.
 */
#ifndef __DESIGN_1_IC_2_PARAM_H__
#define __DESIGN_1_IC_2_PARAM_H__


/* Module W Noise1 - White Noise*/
#define MOD_WNOISE1_COUNT                              3
#define MOD_WNOISE1_DEVICE                             "IC2"
#define MOD_WNOISE1_ALG0_ENABLENOISE_ADDR              0
#define MOD_WNOISE1_ALG0_ENABLENOISE_FIXPT             0x00000000
#define MOD_WNOISE1_ALG0_ENABLENOISE_VALUE             SIGMASTUDIOTYPE_FIXPOINT_CONVERT(0)
#define MOD_WNOISE1_ALG0_ENABLENOISE_TYPE              SIGMASTUDIOTYPE_FIXPOINT
#define MOD_WNOISE1_ALG0_SEED_ADDR                     1
#define MOD_WNOISE1_ALG0_SEED_FIXPT                    0x0005464B
#define MOD_WNOISE1_ALG0_SEED_VALUE                    SIGMASTUDIOTYPE_INTEGER_CONVERT(345675)
#define MOD_WNOISE1_ALG0_SEED_TYPE                     SIGMASTUDIOTYPE_INTEGER
#define MOD_WNOISE1_ALG0_SEED_ADDR                     1
#define MOD_WNOISE1_ALG0_SEED_FIXPT                    0x0005464B
#define MOD_WNOISE1_ALG0_SEED_VALUE                    SIGMASTUDIOTYPE_INTEGER_CONVERT(345675)
#define MOD_WNOISE1_ALG0_SEED_TYPE                     SIGMASTUDIOTYPE_INTEGER

/* Module Gain1 - Gain*/
#define MOD_GAIN1_COUNT                                1
#define MOD_GAIN1_DEVICE                               "IC2"
#define MOD_GAIN1_GAIN1940ALGNS3_ADDR                  2
#define MOD_GAIN1_GAIN1940ALGNS3_FIXPT                 0x00800000
#define MOD_GAIN1_GAIN1940ALGNS3_VALUE                 SIGMASTUDIOTYPE_FIXPOINT_CONVERT(1)
#define MOD_GAIN1_GAIN1940ALGNS3_TYPE                  SIGMASTUDIOTYPE_FIXPOINT

#endif

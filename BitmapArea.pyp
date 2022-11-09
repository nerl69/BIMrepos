<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>BasisExamples\BitmapArea.py</Name>
        <Title>BitmapArea</Title>
        <Version>1.0</Version>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Test</Text>

        <Parameter>
            <Name>GeneralSettings</Name>
            <Text>General settings</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Length</Name>
                <Text>Length</Text>
                <Value>1000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Width</Name>
                <Text>Width</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>BitmapName</Name>
                <Text>Bitmap name</Text>
                <Value>Auto01.tif</Value>
                <ValueType>String</ValueType>
            </Parameter>
            <Parameter>
                <Name>BitmapNameRow</Name>
                <Text>Bitmap name</Text>
                <ValueType>Row</ValueType>
                <Parameter>
                    <Name>BitmapName</Name>
                    <Text></Text>
                    <Value>Auto01.tif</Value>
                    <ValueType>String</ValueType>
                    <ValueDialog>BitmapResourceDialog</ValueDialog>
                </Parameter>
            </Parameter>
            <Parameter>
                <Name>XScalingFactor</Name>
                <Text>Scaling factor X</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>YScalingFactor</Name>
                <Text>               Y</Text>
                <Value>1.0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>UseMetricalValues</Name>
                <Text>Use metrical values</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>UseRepeatTile</Name>
                <Text>Use repeat tile</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>RotationAngle</Name>
                <Text>Rotation angle</Text>
                <Value>0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>

            <Parameter>
                <Name>UseDirectionToReferenceLine</Name>
                <Text>Use direction to reference line</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>DirectionToReferenceLine</Name>
                <Text>Direction to ref line</Text>
                <Value>1</Value>
                <ValueList>1|2|3|4</ValueList>
                <Visible>UseDirectionToReferenceLine == True</Visible>
                <ValueType>IntegerComboBox</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>Transparency</Name>
            <Text>Transparency</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>TransparentAlpha</Name>
                <Text>Transparent value in %</Text>
                <Value>0</Value>
                <ValueType>Integer</ValueType>
            </Parameter>

            <Parameter>
                <Name>UsePixelMask</Name>
                <Text>Use pixel mask</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>TransparentRed</Name>
                <Text>Transparent color red</Text>
                <Value>0</Value>
                <Visible>UsePixelMask == True</Visible>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>TransparentGreen</Name>
                <Text>Transparent  color green</Text>
                <Value>0</Value>
                <Visible>UsePixelMask == True</Visible>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>TransparentBlue</Name>
                <Text>Transparent  color blue</Text>
                <Value>0</Value>
                <Visible>UsePixelMask == True</Visible>
                <ValueType>Integer</ValueType>
            </Parameter>
            <Parameter>
                <Name>TransparentColorTolerance</Name>
                <Text>Transparent color tolerance</Text>
                <Value>0</Value>
                <Visible>UsePixelMask == True</Visible>
                <ValueType>Integer</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Translation</Name>
            <Text>Translation</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>XOffset</Name>
                <Text>Offset X</Text>
                <Value>0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
            <Parameter>
                <Name>YOffset</Name>
                <Text>       Y</Text>
                <Value>0</Value>
                <ValueType>Double</ValueType>
            </Parameter>
        </Parameter>


        <Parameter>
            <Name>UseReferencePoint</Name>
            <Text>Define reference point</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReferencePointX</Name>
            <Text>Reference point X</Text>
            <Value>0.0</Value>
            <Visible>UseReferencePoint == 1</Visible>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>ReferencePointY</Name>
            <Text>Reference point Y</Text>
            <Value>0.0</Value>
            <Visible>UseReferencePoint == 1</Visible>
            <ValueType>Length</ValueType>
        </Parameter>

    </Page>
</Element>

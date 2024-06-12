<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:cmd="http://www.clarin.eu/cmd/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs math" version="3.0">
    <xsl:output indent="yes" omit-xml-declaration="no"/>
     <xsl:param name="json-uri" select="()"/>
    <xsl:param name="json" select="unparsed-text($json-uri)"/>
    <xsl:param name="json-xml" select="json-to-xml($json)"/>


    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>


    <!-- template for the first tag -->

    <xsl:template match="cmd:Assessement" xpath-default-namespace="http://www.w3.org/2005/xpath-functions">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="node()"/>
            <cmd:Review>
                <cmd:author><xsl:value-of select="$json-xml//array[@key='reviews']/map/map[@key='author']/string[@key='name']"/></cmd:author>
                <cmd:published><xsl:value-of select="$json-xml//array[@key='reviews']/map/string[@key='datePublished']"/></cmd:published>
                <cmd:body><xsl:value-of select="$json-xml//array[@key='reviews']/map/string[@key='reviewBody']"/></cmd:body>
                <cmd:rating><xsl:value-of select="$json-xml//array[@key='reviews']/map/map[@key='reviewRating']/number[@key='ratingValue']"/></cmd:rating>
                <xsl:for-each select="$json-xml//array[@key='interactionStatistic']/map">
                    <xsl:if test="./string[@key='interactionType' and text() ='LikeAction']">
                        <cmd:like><xsl:value-of select="./string[@key='interactionType' and text() ='LikeAction']/following-sibling::map/string[@key='name']"/></cmd:like>
                    </xsl:if>
                    <xsl:if test="./string[@key='interactionType' and text() ='DislikeAction']">
                        <cmd:dislike><xsl:value-of select="./string[@key='interactionType' and text() ='DislikeAction']/following-sibling::map/string[@key='name']"/></cmd:dislike>
                    </xsl:if>
                </xsl:for-each>
            </cmd:Review>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>

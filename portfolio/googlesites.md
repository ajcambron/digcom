---
title: Google Sites
parent: Portfolio
---
# Google Sites
## WYSIWYG
The platform we will be using to create a website is [Google Sites](https://sites.google.com). This website allows for WYSIWYG (What you see is what you get) website design. This is the easiest way to quickly design sites for the web, without needing to know how to write HTML (the language of websites).

To create a new site head to [sites.google.com](https://sites.google.com) and create a new blank page. From here, you can begin to create a webpage to host your design content.

{% include googlesites-create.html %}

### Adding Text
#### Creating a Text Box
There are multiple ways to create a text box in Google Sites. The simplest way is to click on the insert a text box from the **Insert** options on the sidebar.

{% include googlesites-insert.html %}

Additionally you may using the pre-designed **Content Blocks** that create placeholder text and graphic boxes to help you construct your site.

The third and final way is to double click where you would like to insert text and then select the blue **Tt** text icon that appears.

{% include googlesites-quickmenu.html %}

Select the text box by clicking inside the box until a **Text Cursor** appears. You may then type whatever you wish.

#### Changing Text Settings
In order to adjust text settings click on the **edit pencil** after selecting the text box.

{% include googlesites-edittext.html %}

The controls for editing text will then appear and then allow you to set custom text settings.

{% include googlesites-textsettings.html %}

### Inserting Images
Inserting images works in much the same way as adding text. You can insert images by using the insert menu, content blocks, or double clicking and using the quick menu. Instead of selecting the blue **Tt** icon you will use the red image icon to insert images.

Once an image frame has been added, you can upload images by clicking on the plus icon in the frame.

{% include googlesites-frame.html %}

From here you can insert web-safe image formats onto your website. Acceptable image formats are .PNG and .JPG.
#### Converting Images
In order to convert other image formats like .SVG and .PDF into web-safe formats, open your image on the computer in Preview or the corresponding design software. Export it to .PNG by going to File>Export in the menu bar.

#### Capturing Difficult Images
In order to create web-safe images of computer interfaces or 3d models that do not easily export, another option in to screenshot your work. On a Mac, the command for creating screenshots is (Cmd Shift 4). The screenshot will save to your desktop by default.

### Adjusting Themes and Colors

<div style="float: left; margin: 0 16px 12px 0;">
{% include googlesites-themes.html %}
</div>

To change the look and feel of your site, you will want to customize your site theme. The themes tab on the sidebar contains pre-made themes you may use as a starting point for designing your site. You may also create a custom theme in which you make all the design decisions yourself.

<div style="clear: both;"></div>

### Preview Design Changes
By clicking on the picture of a laptop from the menu bar, you can preview what the website will look like when it is published.

{% include googlesites-menubar.html %}

### Publishing
Publishing is the way in which website changes are made visible to others. You may think of publishing as "saving" your final changes so that others may see them. In order to make sure that your changes are visible, you must click the purple <i>Publish</i> button on Google Sites, then after reviewing your changes, you will need to confirm your changes by pressing publish one more time.

#### Submitting
In order to submit a final link to your website, click on the icon of a chain from the menu bar, otherwise known as "Copy Published Site Link". Click <i>copy link</i> and submit the link on the assignment page.

## Advanced Google Site
### Adding Video Content
* Videos have to first be uploaded to Google Drive
* Format needs to be .mp4 H.264
* Insert your video as Google Drive content

### Adding Image Galleries
Multiple images that belong together, a set of process shots, a storyboard, don't need to be stacked one after another down the page. The Image Carousel groups them into a single slideshow instead.

* Insert an Image Carousel the same way you'd insert a single image, from the **Insert** sidebar
* Upload multiple images at once. They play as a slideshow in the order you added them
* Add a caption to each image so a viewer knows what they're looking at
* Choose **Crop to fit** or **Fit to content** depending on whether your images share a size

{% include googlesites-carousel.html %}

### Adding Custom HTML
Google Sites sandboxes embedded content for security, so you can't paste in arbitrary code. What you can do is embed something another tool already built and gave you an embed code for.

* From the **Insert** sidebar, choose **Embed**
* **Embed URL** only needs a link. Google Sites generates the preview automatically
* **Embed code** is for pasting an actual iframe or embed snippet. Figma, Canva, and Google Forms all provide one under their own "Share" or "Embed" options
* Scripts inside an embed code generally won't run. If a tool needs live scripting to function, expect it not to display correctly here

{% include googlesites-embed.html %}

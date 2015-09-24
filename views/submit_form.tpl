<div class="bs-docs-section">
  <div class="row">
    <div class="col-lg-6 col-lg-offset-3">
      <div class="well bs-component">
        <form class="form-horizontal" action="/submit" method="post">
          <fieldset>
            <legend>New Abstract</legend>
            <div class="form-group">
              <label for="name" class="col-lg-2 control-label">Name</label>
              <div class="col-lg-10">
                <input class="form-control" name="name" placeholder="Your name" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="title" class="col-lg-2 control-label">Project</label>
              <div class="col-lg-10">
                <input class="form-control" name="title" placeholder="Title of your PhD project" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="authors" class="col-lg-2 control-label">Supervisors</label>
              <div class="col-lg-10">
                <input class="form-control" name="authors" placeholder="Names of your supervisors" type="text"></input>
              <!--  <span class="help-block">Add an asterisk to the name of the corresponding author. Please use ; (semicolon) as a delimiter where the example does.</span>-->
              </div>
            </div>
            <div class="form-group">
              <label for="affils" class="col-lg-2 control-label">Affiliations</label>
              <div class="col-lg-10">
                <input class="form-control" name="affils" placeholder="TiCC and/or any other affiliations" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="contact" class="col-lg-2 control-label">E-mail</label>
              <div class="col-lg-10">
                <input class="form-control" name="contact" placeholder="mail@tilburguniversity.edu OR mail@uvt.nl" type="text"></input>
              <!--  <span class="help-block">Use the same order as the authors for both affiliations and contact.</span>-->
              </div>
            </div>
            <div class="form-group">
              <label for="title" class="col-lg-2 control-label">Website</label>
              <div class="col-lg-10">
                <input class="form-control" name="site" placeholder="A website of your project (if any)" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="text" class="col-lg-2 control-label">Abstract</label>
              <div class="col-lg-10">
                <textarea class="form-control" rows="10" name="text" placeholder="Abstract text, 200-300 words.&#10;&#10;Please do not break sentences with a newline, or use \ (backslash) in running text; your abstract might not compile.&#10;&#10;Please avoid using references, we promise not to reject your abstract."></textarea>
                <!--<span class="help-block">You can provide references in a non-square bracket notation as such: <br /><br />abstract text...<br /><br />References:<br />first reference<br />second reference<br />etc.</span>-->
              </div>
            </div>
              <!--
                <textarea class="form-control" rows="10" name="text" placeholder="Abstract text. Can include LaTeX commands, so please don't use \ (backslash) in running text; your abstract might not compile."></textarea>
              </div>
            </div>
            <div class="form-group">
              <label for="ref" class="col-lg-2 control-label">References</label>
              <div class="col-lg-10">
                <textarea class="form-control" rows="6" name="ref" placeholder="BiBTeX references, labels have to correspond to those used in the \cite commands."></textarea>
                <span class="help-block">BibTeX refrences can for example be found in Google Scholar under 'cite'.</span>
              </div>
            </div>
            <legend>Objects</legend>
            <span class="help-block">Leave any field empty if not applicable.</span>
            <div class="form-group">
              <label for="figurl" class="col-lg-2 control-label">Figure</label>
              <div class="col-lg-10">
                <input class="form-control" name="figurl" placeholder="URL to some PNG or JPG." type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="table" class="col-lg-2 control-label">Tabular</label>
              <div class="col-lg-10">
                <textarea class="form-control" rows="6" name="ref" placeholder="LaTeX code for tabular, no need to specify the table environment!"></textarea>
              </div>
            </div>
            <div class="form-group">
              <label for="FigCap" class="col-lg-2 control-label">Caption</label>
              <div class="col-lg-10">
                <input class="form-control" name="figcap" placeholder="This describes the figure in a full sentence." type="text"></input>
              </div>
            </div> -->
            <legend></legend>
            <div class="form-group">
              <div class="col-lg-10 col-lg-offset-2">
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </div>
          </fieldset>
        </form>
      <div style="display: none;" name="source-button" class="btn btn-primary btn-xs">&lt; &gt;</div></div>
    </div>    
  </div>
</div>

<div class="bs-docs-section">
  <div class="row">
    <div class="col-lg-6 col-lg-offset-3">
      <div class="well bs-component">
        <form class="form-horizontal" action="/edit" method="post">
          <fieldset>
            <legend>Your Abstract</legend>
            <div class="form-group">
              <label for="title" class="col-lg-2 control-label">Title</label>
              <div class="col-lg-10">
                <input class="form-control" name="title" value="{{var['title']}}" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="authors" class="col-lg-2 control-label">Authors</label>
              <div class="col-lg-10">
                <input class="form-control" name="authors" value="{{var['authors']}}" type="text"></input>
                <span class="help-block">Add an asterisk to the name of the corresponding author. Please use ; (semicolon) as a delimiter where the example does.</span>
              </div>
            </div>
            <div class="form-group">
              <label for="affils" class="col-lg-2 control-label">Affiliations</label>
              <div class="col-lg-10">
                <input class="form-control" name="affils" value="{{var['affiliations']}}" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <label for="contact" class="col-lg-2 control-label">Contact</label>
              <div class="col-lg-10">
                <input class="form-control" name="contact" value="{{var['contact']}}" type="text"></input>
                <span class="help-block">Use the same order as the authors for both affiliations and contact.</span>
              </div>
            </div>
            <div class="form-group">
              <label for="text" class="col-lg-2 control-label">Abstract</label>
              <div class="col-lg-10">
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
            </div>
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
